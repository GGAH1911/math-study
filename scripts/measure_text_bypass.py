#!/usr/bin/env python3
"""식-텍스트 우회 회수율 측정 — 이미지로 escalate된 문제(solved_by≠haiku)를
searchable_text(텍스트)만으로 Haiku가 푸나? 회수되면 = 그건 vision 누명이었다는 뜻.
검증 = ans==gold. 회수율은 텍스트 품질에 의존(=하한). 측정 전용(md 안 고침).
환경: MTB_N(80), MTB_WORKERS(5)."""
from __future__ import annotations
import re, json, os, subprocess, glob, random
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
N = int(os.environ.get('MTB_N', '80'))
WORKERS = int(os.environ.get('MTB_WORKERS', '5'))
random.seed(11)


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    st = re.search(r'^searchable_text:\s*\|\s*\n(.*?)(?=^\S|\Z)', t, re.M | re.S)
    return dict(ans=g('answer'), fmt=g('format'), sb=g('solved_by'), st=(st.group(1).strip() if st else ''))


def candidates():
    out = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        m = meta(Path(f).read_text(encoding='utf-8'))
        if m['sb'] not in ('sonnet', 'opus'):          # 이미지-Haiku가 실패한 것만
            continue
        if not m['ans'] or not m['st']:
            continue
        if m['fmt'] == 'choice' and '①' not in m['st']:  # 보기 없으면 제외(매핑 불가)
            continue
        out.append((Path(f).stem, m))
    return out


def solve_text(m):
    ft = '객관식 5지선다' if m['fmt'] == 'choice' else '단답형(정수)'
    want = '보기번호 1-5 정수' if m['fmt'] == 'choice' else '정수'
    p = (f"다음은 한국 수능 수학 문제다 (형식: {ft}).\n\n{m['st']}\n\n"
         f'이 문제를 끝까지 풀어라. 풀이·설명 없이 마지막에 오직 ```json\n{{"answer": <{want}>}}\n``` 만.')
    args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--max-turns', '4', '--output-format', 'json', '--', p]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=150)
        env = json.loads(r.stdout)
    except Exception:
        return None, 0.0
    txt = env.get('result', '') or ''
    cost = env.get('total_cost_usd', 0) or 0.0
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip(), cost
        except Exception:
            pass
    return None, cost


def main():
    cand = candidates(); random.shuffle(cand); tg = cand[:N]
    print(f"═══ 식-텍스트 우회 회수율 (이미지-escalate {len(cand)}개 중 {len(tg)} 샘플) ═══")
    print(f"  층: {dict(Counter((m['fmt'], m['sb']) for _, m in tg))}\n", flush=True)
    rec = []; tot = 0.0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(solve_text, m): (stem, m) for stem, m in tg}
        for fut in as_completed(futs):
            stem, m = futs[fut]; a, c = fut.result(); tot += c; ok = (a == m['ans']); rec.append((m['fmt'], m['sb'], ok))
            print(f"  {stem:34s} [{m['sb']}/{m['fmt']}] 답 {str(a):>4} {'✅회수' if ok else '✗'}", flush=True)
    n = max(1, len(rec)); r = sum(1 for *_, ok in rec if ok)
    print(f"\n═══ 결과 ═══ ${tot:.2f}", flush=True)
    print(f"  텍스트로 회수: {r}/{n} = {100*r//n}%  (= 이미지-escalate의 최소 {100*r//n}%가 vision 누명)", flush=True)
    tota = Counter(); good = Counter()
    for fmt, sb, ok in rec:
        tota[(fmt, sb)] += 1; good[(fmt, sb)] += ok
    for k in sorted(tota):
        print(f"    {k[1]}/{k[0]}: {good[k]}/{tota[k]}", flush=True)
    print(f"  (회수율은 텍스트 품질 의존 → 하한. 못 회수 = 도형의존 + 진짜 수학hard + 텍스트결함)", flush=True)


if __name__ == '__main__':
    main()
