# 2020 9월모평 나형 03 (대응 그림): (g∘f)(1)?  (보기 ③=3)
# 그림 판독 — f: X→Y, g: Y→X
f = {1: 4, 2: 2, 3: 5}
g = {2: 1, 4: 3, 5: 2}
CANDIDATE = 3
print('VERIFY_PASS' if g[f[1]] == CANDIDATE else 'VERIFY_FAIL')
