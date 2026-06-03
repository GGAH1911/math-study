from sympy import *

a = Integer(9)
p = Rational(5, 2)

def g(xv):
    xv = Rational(xv)
    if xv <= 0:
        return xv**3 + a*xv**2 + 15*xv + 7
    else:
        return -p*xv**2 + 15*xv + 7

def g_prime_val(tv):
    tv = Rational(tv)
    if tv <= 0:
        return 3*tv**2 + 2*a*tv + 15
    else:
        return -2*p*tv + 15

# 조건 (가) 검증: x=0에서 미분가능
assert g(0) == 7, 'continuity failed'
assert g_prime_val(0) == 15, 'left derivative mismatch'
assert -2*p*0 + 15 == 15, 'right derivative mismatch'

# 조건 (나) 검증: g'(x)*g'(x-4)=0 의 서로 다른 실근 4개
t = symbols('t')
roots_neg_poly = solve(3*t**2 + 2*a*t + 15, t)
roots_neg_valid = [r for r in roots_neg_poly if r <= 0]
root_pos = Rational(15, 2*p)
assert root_pos > 0, 'root_pos must be positive'

A = set(roots_neg_valid) | {root_pos}
A_shift = {r + 4 for r in A}
all_roots = A | A_shift
assert len(all_roots) == 4, f'(나) failed: got {len(all_roots)} roots: {all_roots}'

# 정답 검증
answer = g(-2) + g(2)
assert answer == 32, f'Expected 32, got {answer}'

print('VERIFY_PASS')
