import sympy as sp

n = sp.Symbol('n', positive=True)

# 조건: angle A = 90, AB=2, CA=n
# 각의 이등분선 정리: BD/DC = AB/AC = 2/n
# BC = sqrt(4 + n^2)
# DC = a_n = n/(n+2) * sqrt(4 + n^2)
a_n = n * sp.sqrt(4 + n**2) / (n + 2)

expr = n - a_n

limit_val = sp.limit(expr, n, sp.oo)

if limit_val == 2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {limit_val}')
