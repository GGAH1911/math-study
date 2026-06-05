#!/usr/bin/env python3
"""백필 후 정밀화 — solved_by=opus(객관식)를 더 긴 캡으로 재시도 + timeout/ans-wrong 구분.

배경: 백필 do_api는 timeout과 오답을 모두 'ans-wrong'으로 뭉뚱그렸다. 그래서 solved_by=opus
중 일부는 '진짜 못 푼' 게 아니라 '짧은 캡(90/150s)에 못 끝낸' false-opus일 수 있다.
이 패스는 의심 케이스(opus·choice)만 골라 더 긴 캡(Haiku 180 / Sonnet 300)으로 재시도하고
정확한 사유(answer/timeout/ans-wrong)를 기록한다.
  · 이제 풀리면     → solved_by 내림(haiku/sonnet) = false-opus 교정
  · 오답으로 끝     → confirmed-killer (단단한 킬러)
  · 여전히 timeout  → opus 유지 + refine_status=killer-timeout-capped (시간 더 줘도 못 끝냄)

numeric opus는 검증기 없이 원래부터 ans-wrong 확정 → 제외. solved_by=sonnet(opus캐시 Haiku실패)도
같은 의심이 있으나 영향 작아 v1은 opus만.
멱등: solution 블록에 refine_status 있으면 skip. 백그라운드 로그 관측.
환경: REFINE_EFFORT(medium), REFINE_HAIKU_TO(180), REFINE_SONNET_TO(300), REFINE_WORKERS(3), REFINE_LIMIT.
"""
from __future__ import annotations
import re, sys, json, glob, os, subprocess, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

EFFORT = os.environ.get('REFINE_EFFORT', 'medium')
HAIKU_TO = int(os.environ.get('REFINE_HAIKU_TO', '180'))
SONNET_TO = int(os.environ.get('REFINE_SONNET_TO', '300'))
WORKERS = int(os.environ.get('REFINE_WORKERS', '3'))
LIMIT = int(os.environ.get('REFINE_LIMIT', '0'))
SYSTEM = ("당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부된 문제 이미지를 "
          "Read 도구로 먼저 본 뒤 풀이하세요. 도형·조건·보기 값은 모두 이미지에서 확인합니다. 추측 금지.")


def _f(t, k, d=None):
    m = re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)
    return m.group(1).strip().strip('\'"') if m else d


def strip_prompt(img_paths):
    if len(img_paths) == 1:
        intro = f"문제 이미지: {img_paths[0]}\n문항 형식: 객관식 5지선다\n\n위 이미지를 Read 로 연 뒤"
    else:
        listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(img_paths))
        intro = (f"문제 이미지 — 세로로 길어 {len(img_paths)}장으로 나눴고 경계가 약간 겹칩니다:\n"
                 f"{listing}\n문항 형식: 객관식 5지선다\n\n위 {len(img_paths)}장을 **모두** Read 로 열어 "
                 f"**하나의 문제로 이어 붙여** 본 뒤")
    return (f"{intro} 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** "
            f"풀이·설명 없이 마지막에 오직 하나의 ```json 블록만:\n\n"
            f'```json\n{{"answer": <네가 푼 보기 번호 1-5 정수>}}\n```')


def solve_ex(stem, model, timeout):
    """(ans|None, cost, status) — status ∈ answer / timeout / no-answer / no-img"""
    img = IMGDIR / (stem + '.png')
    if not img.exists():
        return None, 0.0, 'no-img'
    real = img.resolve()
    tiles = [str(t) for t in tile_for_vision(real)]
    args = ['claude', '-p', '--model', model, '--effort', EFFORT,
            '--allowedTools', 'Read', '--add-dir', str(real.parent),
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '14', '--system-prompt', SYSTEM, '--output-format', 'json', '--',
            strip_prompt(tiles)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 0.0, 'timeout'
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
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL) or re.findall(r'(\{[^{}]*"answer"[^{}]*\})', txt, re.DOTALL)):
        try:
            ans = str(json.loads(b).get('answer')).strip()
            break
        except Exception:
            pass
    return ans, cost, ('answer' if ans is not None else 'no-answer')


def find_targets():
    out = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        if not re.search(r'^solution:', t, re.M):
            continue
        if _f(t, 'solved_by') != 'opus':
            continue
        if _f(t, 'format') != 'choice':            # numeric opus 제외(검증기 없이 ans-wrong 확정)
            continue
        if re.search(r'^\s*refine_status:', t, re.M):
            continue                               # 멱등
        out.append((Path(f), Path(f).stem, _f(t, 'answer')))
    return out


def update_md(path, sb, fails, status):
    t = path.read_text(encoding='utf-8')
    block = f"  solved_by: {sb}\n"
    if fails:
        block += "  escalation:\n" + ''.join(f"    - {{model: {m}, reason: {r}}}\n" for m, r in fails)
    block += f"  refine_status: {status}\n"
    # 기존 solved_by 라인 + escalation 블록 제거 후 generated_by 뒤에 재삽입
    t = re.sub(r'^  solved_by:.*\n(  escalation:\n(    - .*\n)+)?', '', t, count=1, flags=re.M)
    t2, n = re.subn(r'(^  generated_by: \w+\n)', lambda m: m.group(1) + block, t, count=1, flags=re.M)
    if n != 1:
        return 'no-anchor'
    path.write_text(t2, encoding='utf-8')
    return 'ok'


def refine(item):
    path, stem, gold = item
    t0 = time.time(); cost = 0.0
    a, c, sa = solve_ex(stem, 'haiku', HAIKU_TO); cost += c
    if a == gold:
        r = update_md(path, 'haiku', [('haiku', 'verify-fail')], 'corrected-haiku')
        return dict(stem=stem, was='opus', now='haiku', status='corrected-haiku', cost=cost, sec=round(time.time() - t0), inj=r)
    a2, c2, sb_ = solve_ex(stem, 'sonnet', SONNET_TO); cost += c2
    if a2 == gold:
        r = update_md(path, 'sonnet', [('haiku', sa), ('sonnet', 'verify-fail')], 'corrected-sonnet')
        return dict(stem=stem, was='opus', now='sonnet', status='corrected-sonnet', cost=cost, sec=round(time.time() - t0), inj=r)
    # 둘 다 실패 → opus 확정. 사유 정밀화 + confirmed vs timeout-capped 구분
    ha = 'ans-wrong' if sa == 'answer' else sa     # 'answer'(오답) → ans-wrong
    so = 'ans-wrong' if sb_ == 'answer' else sb_
    status = 'confirmed-killer' if ('ans-wrong' in (ha, so)) else 'killer-timeout-capped'
    r = update_md(path, 'opus', [('haiku', ha), ('sonnet', so)], status)
    return dict(stem=stem, was='opus', now='opus', status=status, cost=cost, sec=round(time.time() - t0), inj=r)


def main():
    tg = find_targets()
    if LIMIT:
        tg = tg[:LIMIT]
    print(f"═══ opus 정밀화 (effort={EFFORT}, Haiku {HAIKU_TO}s / Sonnet {SONNET_TO}s) ═══", flush=True)
    print(f"  대상(solved_by=opus·choice·미정밀): {len(tg)}개\n", flush=True)
    if not tg:
        print("  대상 없음 (백필 미완 or 이미 정밀화됨)", flush=True)
        return
    res = []; tot = 0.0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(refine, it): it for it in tg}):
            r = fut.result(); res.append(r); tot += r['cost']
            arrow = '✅내림' if r['now'] != 'opus' else ('🔒확정' if r['status'] == 'confirmed-killer' else '⏱캡')
            print(f"  [{len(res)}/{len(tg)}] {r['stem']:30s} opus→{r['now']} {arrow} ({r['status']}) ${r['cost']:.4f} {r['sec']}s {r['inj']}", flush=True)
    from collections import Counter
    by = Counter(r['status'] for r in res)
    corrected = sum(1 for r in res if r['now'] != 'opus')
    print(f"\n═══ 완료 ═══  {len(res)}개 · ${tot:.2f}", flush=True)
    print(f"  교정(false-opus 내림): {corrected}개  |  {dict(by)}", flush=True)
    print(f"  → opus 중 {100 * corrected / len(res):.0f}%가 사실 false-opus(짧은 캡 탓)였음" if res else '', flush=True)


if __name__ == '__main__':
    main()
