# 2020 수능 나형 04 (대응 그림): (g∘f)(1)?  (보기 ⑤=9)
# 그림 판독 — f: X→X, g: X→X  (X={1,3,5,7,9})
f = {1: 5, 3: 1, 5: 9, 7: 3, 9: 7}
g = {1: 3, 3: 5, 5: 9, 7: 1, 9: 7}
CANDIDATE = 9
print('VERIFY_PASS' if g[f[1]] == CANDIDATE else 'VERIFY_FAIL')
