import sympy as sp

def in_A(x, k):
    x = sp.Integer(x)
    if x + 1 <= 0:
        return False
    return sp.N(sp.log(x + 1, 2) - k, 50) <= 0

def in_B(x):
    x = sp.Integer(x)
    if x - 2 <= 0 or x + 1 <= 0:
        return False
    expr = sp.log(x - 2, 2) - sp.log(x + 1, sp.Rational(1, 2)) - 2
    return sp.N(expr, 50) >= 0

ans = None
for k in range(1, 30):
    cnt = sum(1 for x in range(-1, 2**k + 2) if in_A(x, k) and in_B(x))
    if cnt == 5:
        ans = k
        break

if ans is not None:
    cnt = sum(1 for x in range(-1, 2**ans + 2) if in_A(x, ans) and in_B(x))
    print('VERIFY_PASS' if cnt == 5 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
