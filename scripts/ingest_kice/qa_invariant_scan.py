#!/usr/bin/env python3
"""결정론적 불변식 스캐너 — decoded_all.jsonl(전 문제 디코드)을 비전 없이 구조적으로 검사.
red-flag가 0이면 '구조적'으로 결정론 보장(의미 정확성은 별개). 실행마다 동일 결과(결정론)."""
import json, re
from collections import Counter, defaultdict


def violations(t):
    v = []
    if any(0xE000 <= ord(c) <= 0xF8FF for c in t):
        v.append('PUA잔존')                          # 매핑 실패(있으면 안 됨)
    s = re.sub(r'\\[{}]', '', t)                      # 이스케이프 \{ \} 제외 후 괄호 균형
    if s.count('{') != s.count('}'):
        v.append('중괄호불균형')                       # malformed LaTeX
    if re.search(r'\\overline\{[\d.]+\}', t):
        v.append('overline숫자(분수의심)')             # \overline{2} = 깨진 분수 의심
    if re.search(r'\\frac\{[\d.]+\s+[\d.]', t):
        v.append('표garble분수')                       # \frac{1.0 0.3413} = 표 garble(이젠 array여야)
    if re.search(r'\\(frac|sqrt|overline|vec)\{\s*\}', t) or '\\frac{}{}' in t:
        v.append('빈구조')
    if re.search(r'\\begin\{(array|cases|pmatrix)\}\s*\\end', t):
        v.append('빈환경')
    if '확인사항' in t or '답안지' in t or '확확' in t or '사사항항' in t:
        v.append('footer/글자중복')
    if '━' in t or '──' in t or '——' in t:
        v.append('구분선쓰레기')                        # ━ 또는 ──
    if re.search(r'_\{[^{}]*\}_\{|\^\{[^{}]*\}\^\{', t):
        v.append('이중첨자(malformed)')  # 같은 연산자 중복만(_{}_{} / ^{}^{}); super+sub 조합은 정상
    ko = re.findall(r'[가-힣]', t)
    if len(ko) > 20:
        dup = sum(1 for i in range(1, len(t)) if t[i] == t[i-1] and '가' <= t[i] <= '힣')
        if dup / len(ko) > 0.15:
            v.append('한글doubling')
    return v


rows = [json.loads(l) for l in open('/tmp/vision_qa/decoded_all.jsonl')]
cat = Counter(); samp = defaultdict(list); nflag = 0
for r in rows:
    vs = violations(r['text'])
    if vs:
        nflag += 1
        for x in vs:
            cat[x] += 1
            if len(samp[x]) < 6:
                samp[x].append(r['id'].split('/')[-1])
print(f'=== 전수 결정론 불변식 스캔: {len(rows)}문제 ===')
print(f'위반 문제: {nflag}/{len(rows)} ({100 * nflag // max(len(rows), 1)}%)')
for k, n in cat.most_common():
    print(f'  {k}: {n}  예: {samp[k]}')
