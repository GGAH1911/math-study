#!/usr/bin/env python3
"""Phase 0 파일럿 — solved_by 백필의 토큰 단가 실측 (측정 전용, md 안 고침).

choice + (sonnet|opus) 캐시 N개에 '답안전용 스트립' Haiku 호출을 날려
`claude -p --output-format json` 의 usage/cost 를 캡처하고, 답이 gold와 맞는지 확인.
→ 문제당 평균/합계/727 외삽 + Haiku 답일치율 보고.

핵심: 실제 백필이 돌릴 것과 같은 호출(Haiku/high, Read로 이미지 로드, 에이전트 루프)을
그대로 재현해 *실토큰*을 잰다. 단, 출력은 정답 하나만 요구해 출력토큰 최소화.

환경변수: PILOT_N(기본 20), PILOT_WORKERS(기본 3), SOLVE_TIMEOUT(기본 480).
파일을 쓰지 않으므로 안전. 백그라운드 권장.
"""
from __future__ import annotations
import re, sys, json, glob, os, subprocess, time, statistics as st
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

TIMEOUT_S = int(os.environ.get('SOLVE_TIMEOUT', '480'))
N = int(os.environ.get('PILOT_N', '20'))
WORKERS = int(os.environ.get('PILOT_WORKERS', '3'))
EFFORT = os.environ.get('PILOT_EFFORT', 'high')   # low/medium/high — thinking 예산
SYSTEM = ("당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부된 문제 이미지를 "
          "Read 도구로 먼저 본 뒤 풀이하세요. 도형·조건·보기 값은 모두 이미지에서 확인합니다. 추측 금지.")


def _f(t, k, default=None):
    m = re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)
    return m.group(1).strip().strip('\'"') if m else default


def select():
    cands = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        if _f(t, 'format') != 'choice':
            continue
        gb = (re.search(r'^\s*generated_by:\s*(\w+)', t, re.M) or [None, None])[1]
        if gb not in ('sonnet', 'opus'):
            continue
        cands.append(dict(stem=Path(f).stem, gb=gb, gold=_f(t, 'answer'),
                          fig=_f(t, 'has_figure') == 'true', round=Path(f).parent.name))
    # 대표성: figure·sonnet/opus·회차 섞어 정렬 후 균등 N 샘플
    cands.sort(key=lambda c: (c['fig'], c['gb'], c['round'], c['stem']))
    if len(cands) <= N:
        return cands, len(cands)
    step = len(cands) / N
    return [cands[int(i * step)] for i in range(N)], len(cands)


def strip_prompt(img_paths):
    if len(img_paths) == 1:
        intro = f"문제 이미지: {img_paths[0]}\n문항 형식: 객관식 5지선다\n\n위 이미지를 Read 로 연 뒤"
    else:
        listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(img_paths))
        intro = (f"문제 이미지 — 세로로 길어 위→아래 {len(img_paths)}장으로 나눴고 경계가 약간 겹칩니다:\n"
                 f"{listing}\n문항 형식: 객관식 5지선다\n\n"
                 f"위 {len(img_paths)}장을 **모두** Read 로 열어 **하나의 문제로 이어 붙여** 본 뒤")
    return (f"{intro} 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** "
            f"풀이 과정·설명은 쓰지 말고 **마지막에 오직 하나의 ```json 블록**만 출력:\n\n"
            f'```json\n{{"answer": <네가 푼 보기 번호 1-5 정수>}}\n```')


def measure_one(c):
    img = IMGDIR / (c['stem'] + '.png')
    if not img.exists():
        return {**c, 'err': 'no-img'}
    real = img.resolve()
    tiles = [str(t) for t in tile_for_vision(real)]
    args = ['claude', '-p', '--model', 'haiku', '--effort', EFFORT,
            '--allowedTools', 'Read', '--add-dir', str(real.parent),
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '14', '--system-prompt', SYSTEM,
            '--output-format', 'json', '--', strip_prompt(tiles)]
    t0 = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return {**c, 'err': 'timeout', 'sec': TIMEOUT_S}
    dt = round(time.time() - t0)
    try:
        env = json.loads(r.stdout)
    except Exception:
        m = re.findall(r'\{.*\}', r.stdout, re.DOTALL)
        try:
            env = json.loads(m[-1]) if m else {}
        except Exception:
            env = {}
    if not env or env.get('is_error'):
        return {**c, 'err': f"cli:{(env.get('subtype') or r.returncode)}", 'sec': dt}
    u = env.get('usage', {}) or {}
    txt = env.get('result', '') or ''
    ans = None
    blk = re.findall(r'```json\s*(.*?)```', txt, re.DOTALL) or re.findall(r'(\{[^{}]*"answer"[^{}]*\})', txt, re.DOTALL)
    for b in reversed(blk):
        try:
            ans = str(json.loads(b).get('answer')).strip()
            break
        except Exception:
            pass
    inp, out = u.get('input_tokens', 0), u.get('output_tokens', 0)
    cr, cc = u.get('cache_read_input_tokens', 0), u.get('cache_creation_input_tokens', 0)
    return {**c, 'tiles': len(tiles), 'in': inp, 'out': out, 'cache_read': cr, 'cache_creation': cc,
            'total_tok': inp + out + cr + cc, 'cost': env.get('total_cost_usd', 0) or 0,
            'turns': env.get('num_turns', 0), 'sec': dt, 'ans': ans, 'match': ans == c['gold']}


def main():
    pick, pool = select()
    print(f"═══ Phase 0 파일럿: solved_by 백필 토큰 실측 ═══", flush=True)
    print(f"백필 대상 모집단(choice·sonnet/opus): {pool}개 → 표본 {len(pick)}개 "
          f"(figure {sum(c['fig'] for c in pick)}, opus캐시 {sum(c['gb'] == 'opus' for c in pick)})", flush=True)
    print(f"호출: claude -p --model haiku --effort {EFFORT} (답안전용 스트립) · usage 캡처 · md 안 고침\n", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(measure_one, c): c for c in pick}
        for i, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            if r.get('err'):
                print(f"  [{i}/{len(pick)}] {r['stem']:32s} ERR={r['err']} ({r.get('sec', 0)}s)", flush=True)
            else:
                mk = '✓' if r['match'] else f"✗(gold={r['gold']})"
                print(f"  [{i}/{len(pick)}] {r['stem']:32s} tiles={r['tiles']} in={r['in']} out={r['out']} "
                      f"cR={r['cache_read']} tot={r['total_tok']} ${r['cost']:.4f} {r['turns']}t {r['sec']}s ans={r['ans']}{mk}", flush=True)
    ok = [r for r in results if not r.get('err')]
    if not ok:
        print("\n❌ 전부 실패 — usage 캡처 점검 필요", flush=True)
        return
    avg = lambda k: sum(r[k] for r in ok) / len(ok)
    tot = lambda k: sum(r[k] for r in ok)
    matches = sum(r['match'] for r in ok)
    print(f"\n═══ 집계 ({len(ok)}/{len(pick)} 성공, 에러 {len(results) - len(ok)}) ═══", flush=True)
    print(f"  문제당 평균: in={avg('in'):.0f} out={avg('out'):.0f} cache_read={avg('cache_read'):.0f} "
          f"총={avg('total_tok'):.0f}토큰 · ${avg('cost'):.4f} · {avg('turns'):.1f}턴 · {avg('sec'):.0f}s", flush=True)
    print(f"  총토큰 중앙값: {st.median([r['total_tok'] for r in ok]):.0f} / 최대: {max(r['total_tok'] for r in ok)}", flush=True)
    print(f"  표본 {len(ok)}개 합: {tot('total_tok'):,}토큰 · ${tot('cost'):.3f}", flush=True)
    print(f"  ⇒ 727개 외삽: ~{int(avg('total_tok') * 727):,}토큰 · ~${avg('cost') * 727:.2f}", flush=True)
    print(f"  Haiku 답일치율: {matches}/{len(ok)} ({100 * matches / len(ok):.0f}%) "
          f"— 높을수록 escalation이 '검증기 탓'(Haiku가 답은 맞힘) 확정", flush=True)


if __name__ == '__main__':
    main()
