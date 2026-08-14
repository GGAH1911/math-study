#!/usr/bin/env python3
"""'단일샷 실패 → Haiku 반복 성공' 실증 (제일 어려운 confirmed-killer 1개).
A) pass@k    : Haiku 단일샷(Read만·코드 차단) k회 → 성공률 = 현 파이프라인의 난이도 측정 방식.
B) 반복+도구 : Haiku 에이전트(Read+Bash, sympy로 단계 직접계산) 1회 → 풀리나 + 내부 턴수(=반복 횟수).
C) 검증기    : Haiku write-run-fix(Read+Bash) → 정답 확인 verifier 완성해 VERIFY_PASS 내나 + 턴수.
환경: POC_STEM, POC_K(8). 이미지 익명화(정체 누출 차단)."""
from __future__ import annotations
import re, json, glob, os, subprocess, sys, shutil, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VENV_PY = __import__('os').environ.get('MS_PY', __import__('os').path.expanduser('~/.venvs/ms-ingest/bin/python'))  # ★인제스트 venv(옛 경로·죽은 삼항 제거)
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision           # noqa: E402
from build_solution_cache import run_verifier  # noqa: E402  (FORBIDDEN 체크+실행+VERIFY_PASS)

K = int(os.environ.get('POC_K', '8'))
STEM = os.environ.get('POC_STEM', '')


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(ans=g('answer'), fmt=g('format'), et=g('exam_type'), num=g('number'))


def find_meta(stem):
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / (stem + '.md')), recursive=True):
        return meta(Path(f).read_text(encoding='utf-8'))
    return None


def anon(stem):
    img = (IMGDIR / (stem + '.png')).resolve()
    tiles = tile_for_vision(img)
    d = tempfile.mkdtemp(prefix='poc_')
    out = []
    for i, t in enumerate(tiles):
        o = Path(d) / f'p_{i + 1}.png'
        shutil.copy(t, o)
        out.append(str(o))
    return out, d


def listing(tiles):
    return '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))


def call(prompt, add_dir, tools, turns, timeout):
    args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--allowedTools', tools,
            '--add-dir', add_dir, '--max-turns', str(turns), '--output-format', 'json', '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        env = json.loads(r.stdout)
    except Exception:
        return dict(raw='', turns=0, cost=0.0)
    return dict(raw=env.get('result', '') or '', turns=env.get('num_turns', 0), cost=env.get('total_cost_usd', 0) or 0.0)


def ans_of(txt):
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip()
        except Exception:
            pass
    return None


def main():
    stem = STEM or '2022_수능_미적분_23'
    m = find_meta(stem)
    if not m:
        print(f"메타 못찾음: {stem}"); return
    gold, fmt = m['ans'], m['fmt']
    ft = '객관식 5지선다' if fmt == 'choice' else '단답형(정수)'
    tiles, d = anon(stem)
    print(f"═══ PoC: 단일샷 실패 → Haiku 반복 성공 ═══", flush=True)
    print(f"  대상: {stem} ({m['et']} #{m['num']}, {fmt}) · 정답 {gold} · 타일 {len(tiles)}장(익명화)\n", flush=True)
    tot = 0.0

    # ── A. pass@k (단일샷, Read만, 코드 차단) ──
    print(f"── A. pass@{K}  (Haiku 단일샷 · 현 난이도 측정 방식) ──", flush=True)
    pA = (f"문제 이미지:\n{listing(tiles)}\n형식: {ft}\n\n위 이미지를 Read로 연 뒤 끝까지 풀어라. "
          f'풀이·설명 없이 마지막에 오직 ```json\n{{"answer": <정수>}}\n``` 만.')
    succ = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(call, pA, d, 'Read', 12, 150): i for i in range(K)}
        for k, fut in enumerate(as_completed(futs), 1):
            r = fut.result(); tot += r['cost']; a = ans_of(r['raw'])
            ok = (a == gold); succ += ok
            print(f"    시도 {k}/{K}: 답 {str(a):>5}  {'✅' if ok else '✗'}", flush=True)
    p = succ / K
    print(f"  → pass@{K} = {succ}/{K} = {p*100:.0f}%  (난이도: 단일샷 성공률 {p*100:.0f}% → {'쉬움' if p>0.5 else '어려움(킬러)'})\n", flush=True)

    # ── B. 반복 + 도구 (Read+Bash, sympy로 단계 직접계산) ──
    print(f"── B. 반복+도구  (Haiku 에이전트 · sympy 실행하며 단계별) ──", flush=True)
    pB = (f"문제 이미지:\n{listing(tiles)}\n형식: {ft}\n\n위 이미지를 Read로 본 뒤 **반드시 단계별로** 풀어라. "
          f"머리로만 계산하지 말고 각 단계를 `{VENV_PY}` (sympy 사용 가능)로 Bash 실행해 **직접 계산·검증**하라. "
          f"한 단계도 손으로 건너뛰지 마라(건너뛰기가 단일샷 실패의 원인이다). 막히면 다시 계산해 교정하라. "
          f'최종 답을 ```json\n{{"answer": <정수>}}\n``` 로.')
    rB = call(pB, d, 'Read,Bash', 30, 420); tot += rB['cost']
    aB = ans_of(rB['raw']); okB = (aB == gold)
    print(f"  → 답 {aB}  {'✅ 풀림' if okB else '✗ 실패'}  · 내부 턴(반복) {rB['turns']}회  ${rB['cost']:.3f}\n", flush=True)

    # ── C. 검증기 write-run-fix (Read+Bash) ──
    print(f"── C. 검증기  (Haiku write-run-fix · Opus 승격 없이) ──", flush=True)
    pC = (f"문제 이미지:\n{listing(tiles)}\n이 문제의 정답: {gold}\n\n위 이미지를 Read로 본 뒤, 정답 {gold}이 옳음을 "
          f"**독립적으로 확인하는 파이썬 검증 스크립트**를 작성하라. 스크립트는 문제의 원래 조건/식에 정답을 대입해 "
          f"모순이 없으면 마지막 줄에 정확히 `VERIFY_PASS`를 print 해야 한다. 반드시 `{VENV_PY}`로 **직접 실행**해 보고, "
          f"에러나 VERIFY_PASS 미출력이면 고쳐서 다시 실행하라(작동할 때까지 반복). import os/open/subprocess 금지, sympy만. "
          f"완성된 최종 코드를 ```python ... ``` 한 블록으로 제시하라.")
    rC = call(pC, d, 'Read,Bash', 30, 420); tot += rC['cost']
    code = None
    for b in reversed(re.findall(r'```python\s*(.*?)```', rC['raw'], re.DOTALL)):
        code = b.strip(); break
    passed, vout = (run_verifier(code) if code else (False, 'no-code'))
    print(f"  → 검증기 {'완성·VERIFY_PASS ✅' if passed else '미완 ✗ ('+str(vout)[:40]+')'}  · 내부 턴(반복) {rC['turns']}회  ${rC['cost']:.3f}\n", flush=True)

    # ── 결론 ──
    print(f"═══ 결론 ═══  ${tot:.2f}", flush=True)
    print(f"  A 단일샷 난이도 : pass@{K} = {p*100:.0f}%  ({'킬러 확인' if p<0.5 else '의외로 쉬움'})", flush=True)
    print(f"  B 반복+도구     : {'✅ 같은 Haiku가 풀어냄' if okB else '✗ 도구로도 실패(진짜 천장)'} (턴 {rB['turns']})", flush=True)
    print(f"  C 검증기 반복   : {'✅ Haiku가 Opus 없이 완성' if passed else '✗ 미완'} (턴 {rC['turns']})", flush=True)
    verdict = '난이도=Haiku호출수 · 검증기=Haiku반복 둘 다 입증' if (okB and passed) else '부분 입증'
    print(f"  ⇒ {verdict}", flush=True)
    shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    main()
