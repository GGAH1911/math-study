#!/usr/bin/env python3
"""기존 캐시에 solved_by(난이도=최초로 답 맞힌 모델) + escalation 백필.

규칙:
  · 단답형(검증기 없음): generated_by가 곧 solved_by. escalation은 사다리에서 더 싼
    모델이 ans-wrong으로 탈락한 것으로 추론. (재호출 0)
  · 객관식 generated_by=haiku: solved_by=haiku. (재호출 0)
  · 객관식 generated_by∈{sonnet,opus}: Haiku를 답안전용(medium·짧은 cap)으로 재호출.
      - Haiku 정답 → solved_by=haiku, escalation=원 모델들 verify-fail(추론: 답은 맞혔으나 검증기 탈락).
      - Haiku 실패/timeout & opus캐시 → Sonnet 재호출 → 맞으면 solved_by=sonnet, 아니면 opus.
      - Haiku 실패 & sonnet캐시 → solved_by=sonnet.
멱등: solved_by 이미 있으면 skip(이어서 재실행 가능). 병렬, 백그라운드 로그 관측.
환경: BACKFILL_LIMIT(테스트 N개, api·no-api 둘 다), BACKFILL_EFFORT(기본 medium),
      BACKFILL_WORKERS(3), HAIKU_TIMEOUT(90), SONNET_TIMEOUT(150), BACKFILL_NO_API(1=재호출 생략).
"""
from __future__ import annotations
import re, sys, json, glob, os, subprocess, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

EFFORT = os.environ.get('BACKFILL_EFFORT', 'medium')
WORKERS = int(os.environ.get('BACKFILL_WORKERS', '3'))
HAIKU_TO = int(os.environ.get('HAIKU_TIMEOUT', '90'))
SONNET_TO = int(os.environ.get('SONNET_TIMEOUT', '150'))
LIMIT = int(os.environ.get('BACKFILL_LIMIT', '0'))
NO_API = os.environ.get('BACKFILL_NO_API') == '1'
SYSTEM = ("당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부된 문제 이미지를 "
          "Read 도구로 먼저 본 뒤 풀이하세요. 도형·조건·보기 값은 모두 이미지에서 확인합니다. 추측 금지.")
KILLER_LADDER = ['sonnet', 'opus']
DEFAULT_LADDER = ['haiku', 'sonnet', 'opus']


def _f(t, k, d=None):
    m = re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)
    return m.group(1).strip().strip('\'"') if m else d


def strip_prompt(img_paths, fmt):
    ansdesc = '보기 번호 1-5 정수' if fmt == 'choice' else '단답형 정답 정수(0-999)'
    label = '객관식 5지선다' if fmt == 'choice' else '단답형(정수 정답)'
    if len(img_paths) == 1:
        intro = f"문제 이미지: {img_paths[0]}\n문항 형식: {label}\n\n위 이미지를 Read 로 연 뒤"
    else:
        listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(img_paths))
        intro = (f"문제 이미지 — 세로로 길어 {len(img_paths)}장으로 나눴고 경계가 약간 겹칩니다:\n"
                 f"{listing}\n문항 형식: {label}\n\n위 {len(img_paths)}장을 **모두** Read 로 열어 "
                 f"**하나의 문제로 이어 붙여** 본 뒤")
    return (f"{intro} 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** "
            f"풀이·설명 없이 마지막에 오직 하나의 ```json 블록만:\n\n"
            f'```json\n{{"answer": <{ansdesc}>}}\n```')


def solve(stem, fmt, model, timeout):
    img = IMGDIR / (stem + '.png')
    if not img.exists():
        return None, 0.0
    real = img.resolve()
    tiles = [str(t) for t in tile_for_vision(real)]
    args = ['claude', '-p', '--model', model, '--effort', EFFORT,
            '--allowedTools', 'Read', '--add-dir', str(real.parent),
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '14', '--system-prompt', SYSTEM, '--output-format', 'json', '--',
            strip_prompt(tiles, fmt)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 0.0
    try:
        env = json.loads(r.stdout)
    except Exception:
        m = re.findall(r'\{.*\}', r.stdout, re.DOTALL)
        try:
            env = json.loads(m[-1]) if m else {}
        except Exception:
            env = {}
    cost = (env or {}).get('total_cost_usd', 0) or 0.0
    txt = (env or {}).get('result', '') or ''
    ans = None
    blk = re.findall(r'```json\s*(.*?)```', txt, re.DOTALL) or re.findall(r'(\{[^{}]*"answer"[^{}]*\})', txt, re.DOTALL)
    for b in reversed(blk):
        try:
            ans = str(json.loads(b).get('answer')).strip()
            break
        except Exception:
            pass
    return ans, cost


def inject(path, solved_by, fails):
    t = path.read_text(encoding='utf-8')
    if re.search(r'^\s*solved_by:', t, re.M):
        return 'already'
    ins = f"  solved_by: {solved_by}\n"
    if fails:
        ins += "  escalation:\n" + ''.join(f"    - {{model: {m}, reason: {r}}}\n" for m, r in fails)
    new, n = re.subn(r'(^  generated_by: \w+\n)', lambda mm: mm.group(1) + ins, t, count=1, flags=re.M)
    if n != 1:
        return 'no-anchor'
    path.write_text(new, encoding='utf-8')
    return 'ok'


def categorize():
    no_api, api = [], []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        if not re.search(r'^solution:', t, re.M):
            continue                                       # 캐시된 것만
        if re.search(r'^\s*solved_by:', t, re.M):
            continue                                       # 이미 백필됨(멱등)
        gb = _f(t, 'generated_by')
        if gb not in ('haiku', 'sonnet', 'opus'):
            continue
        it = (Path(f), Path(f).stem, _f(t, 'format', 'choice'), gb, _f(t, 'answer'), _f(t, 'killer_tier'))
        (no_api if (it[2] != 'choice' or gb == 'haiku') else api).append(it)
    return no_api, api


def infer_noapi(fmt, gb, tier):
    ladder = KILLER_LADDER if tier == 'killer' else DEFAULT_LADDER
    if gb == 'haiku':
        return 'haiku', []
    idx = ladder.index(gb) if gb in ladder else 0
    return gb, [(m, 'ans-wrong') for m in ladder[:idx]]    # 단답 escalation은 ans-wrong 뿐


def do_api(item):
    path, stem, fmt, gb, gold, tier = item
    t0 = time.time()
    if not gold:                                           # 안전망(거의 없음)
        return dict(stem=stem, gb=gb, solved=gb, cost=0.0, sec=0, inj=inject(path, gb, []), ha=None, gold=gold)
    ans, cost = solve(stem, fmt, 'haiku', HAIKU_TO)
    if ans == gold:                                        # Haiku가 답 맞힘 = 원래 검증기 탓 escalate
        fails = [('haiku', 'verify-fail')] + ([('sonnet', 'verify-fail')] if gb == 'opus' else [])
        return dict(stem=stem, gb=gb, solved='haiku', cost=cost, sec=round(time.time() - t0),
                    inj=inject(path, 'haiku', fails), ha=ans, gold=gold)
    if gb == 'opus':                                       # Haiku 실패 → Sonnet 재시도
        ans2, c2 = solve(stem, fmt, 'sonnet', SONNET_TO); cost += c2
        if ans2 == gold:
            return dict(stem=stem, gb=gb, solved='sonnet', cost=cost, sec=round(time.time() - t0),
                        inj=inject(path, 'sonnet', [('haiku', 'ans-wrong'), ('sonnet', 'verify-fail')]), ha=ans, gold=gold)
        return dict(stem=stem, gb=gb, solved='opus', cost=cost, sec=round(time.time() - t0),
                    inj=inject(path, 'opus', [('haiku', 'ans-wrong'), ('sonnet', 'ans-wrong')]), ha=ans, gold=gold)
    return dict(stem=stem, gb=gb, solved='sonnet', cost=cost, sec=round(time.time() - t0),   # sonnet캐시 & Haiku 실패
                inj=inject(path, 'sonnet', [('haiku', 'ans-wrong')]), ha=ans, gold=gold)


def main():
    no_api, api = categorize()
    if LIMIT:
        no_api, api = no_api[:LIMIT], api[:LIMIT]
    print(f"═══ solved_by 백필 (effort={EFFORT}) ═══", flush=True)
    print(f"  재호출 0 (단답·haiku캐시): {len(no_api)} | 재호출 필요(choice sonnet/opus): {len(api)}", flush=True)
    nok = sum(infer_inject(it) for it in no_api)
    print(f"  ✓ no-API 백필 {nok}/{len(no_api)}", flush=True)
    if NO_API:
        print("  (BACKFILL_NO_API=1 — 재호출 생략)", flush=True)
        return
    print(f"  → API 재호출 {len(api)}개 (Haiku {EFFORT} {HAIKU_TO}s, opus캐시 실패시 Sonnet {SONNET_TO}s)\n", flush=True)
    tot, dist, done = 0.0, {'haiku': 0, 'sonnet': 0, 'opus': 0}, 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(do_api, it): it for it in api}):
            r = fut.result(); done += 1; tot += r['cost']; dist[r['solved']] += 1
            print(f"  [{done}/{len(api)}] {r['stem']:30s} {r['gb']}→{r['solved']} "
                  f"{'✓' if r['solved'] == 'haiku' else '↑'} ${r['cost']:.4f} {r['sec']}s {r['inj']}", flush=True)
            if done % 40 == 0:
                print(f"    ··· {done}/{len(api)} 누적 ${tot:.2f} | 분포 {dist}", flush=True)
    print(f"\n═══ 완료 ═══  API {done}개 · 누적 ${tot:.2f}", flush=True)
    print(f"  재호출분 solved_by: haiku {dist['haiku']} / sonnet {dist['sonnet']} / opus {dist['opus']}", flush=True)
    if done:
        print(f"  ⇒ choice escalation 중 {100 * dist['haiku'] / done:.0f}%가 실은 Haiku-solvable(검증기 탓)", flush=True)


def infer_inject(it):
    path, stem, fmt, gb, gold, tier = it
    sb, fails = infer_noapi(fmt, gb, tier)
    return 1 if inject(path, sb, fails) == 'ok' else 0


if __name__ == '__main__':
    main()
