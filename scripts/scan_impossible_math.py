#!/usr/bin/env python3
"""searchable_text에서 '수학적으로 불가능한 값' = 명백한 OCR/전사 버그를 스캔.
정밀도 우선: sin/cos 값(또는 sin·sin 곱)이 1을 초과하는 케이스만 플래그.
비율(`:`) 형태(sin θ1:sin θ2=√3:√2)는 정상이므로 제외, 분모(2/sin…)도 제외.
(#18에서 'sin·sin=3√2/2≈2.12' 발견한 패턴을 전 회차로 일반화.)"""
import re, glob
from pathlib import Path
import sympy as sp

ROOT = Path('/home/insung/Projects/math-study/.claude/worktrees/gallant-tu-2c9be7')


def norm_value(s):
    s = s.strip().strip(' ,')
    s = s.replace('²', '**2').replace('³', '**3').replace('×', '*').replace('·', '*').replace('⋅', '*')
    s = re.sub(r'√\s*\(([^)]+)\)', r'sqrt(\1)', s)
    s = re.sub(r'√\s*(\d+)', r'sqrt(\1)', s)
    s = re.sub(r'(\d)\s*sqrt', r'\1*sqrt', s)
    s = re.sub(r'(\d)\s*\(', r'\1*(', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    return s


def safe_eval(s):
    try:
        e = sp.sympify(norm_value(s))
        if e.free_symbols:
            return None
        return float(sp.N(e))
    except Exception:
        return None


def extract_searchable(text):
    m = re.search(r'^searchable_text:\s*\|\s*\n(.*?)(?=^\S|\Z)', text, re.M | re.S)
    return m.group(1) if m else ''


PAT = re.compile(r'(?P<fn>sin|cos)(?P<mid>[^=\n:]{0,20})=\s*(?P<val>[0-9√(][0-9√()/*.\- ²³]*)')
HANGUL = re.compile(r'[가-힣]')
BAD_MID = ('+', 'dx', 'dy', 'dt', '∫', 'f(', 'g(', '방정식', '직선', '그래프', '점', '함수')


def is_false_positive(st, m):
    fs = m.start('fn')
    pre = st[max(0, fs - 6):fs]
    if '/' in pre or '}' in pre or '+' in pre:           # 분모·분수·합 안의 sin/cos
        return True
    pc = pre.rstrip('\\ ')
    if pc and pc[-1].isalnum():                          # 계수 (3\sin…, a sin…)
        return True
    mid, val = m.group('mid'), m.group('val')
    if HANGUL.search(mid):                               # 문장 경계 넘어 다른 식의 =
        return True
    if any(b in mid for b in BAD_MID):                   # 합(+)·적분(dx)·다른함수
        return True
    if any(b in val for b in ('dx', 'dy', 'dt')):
        return True
    after = st[m.end():m.end() + 4].lstrip()             # 우변이 또 다른 항으로 이어지면
    if after[:1] == '\\' or re.match(r'[a-zA-Z]', after):  # (3\cosθ, 2cos…) → 'trig=수' 아님
        return True
    return False


def scan_file(f):
    st = extract_searchable(Path(f).read_text(encoding='utf-8'))
    hits = []
    for m in PAT.finditer(st):
        if ':' in st[m.end():m.end() + 6]:              # 비율(√3:√2) 형태 → 정상
            continue
        if is_false_positive(st, m):
            continue
        v = safe_eval(m.group('val'))
        if v is not None and abs(v) > 1.0001:           # sin/cos는 |값|≤1만 가능
            frag = re.sub(r'\s+', ' ', (m.group('fn') + m.group('mid') + '=' + m.group('val')).strip())
            ctx = re.sub(r'\s+', ' ', st[max(0, m.start() - 32):m.end() + 12].strip())
            hits.append((frag, round(v, 3), ctx))
    return hits


files = [f for f in sorted(glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)) if 'README' not in f]
print(f"═══ 불가능값 스캔: {len(files)} 문제 (sin/cos > 1) ═══\n")
total = 0
for f in files:
    hits = scan_file(f)
    if hits:
        total += 1
        print(f"🔴 {Path(f).relative_to(ROOT)}")
        for frag, v, ctx in hits:
            print(f"      값 \"{frag}\" ≈ {v}  (사인/코사인 ≤ 1 위반)")
            print(f"      문맥: …{ctx}…")
print(f"\n오탐 필터 후 잔존: {total} 문제")
