from sympy import *

x = symbols('x', positive=True)
f = x**2 - 5*x + 2*ln(x)

# 도함수: f'(x) = (2x-1)(x-2)/x
fp = diff(f, x)

# 임계점: (2x-1)(x-2)=0 => x=1/2, x=2
crit_eq = 2*x**2 - 5*x + 2
crit_pts = solve(crit_eq, x)

# 극대(x=1/2)와 극소(x=2)에서의 t값
t1 = f.subs(x, Rational(1, 2))  # 극대값: -9/4 - 2*ln(2)
t2 = f.subs(x, 2)               # 극소값: -6 + 2*ln(2)

# 합 = (-9/4 - 2ln2) + (-6 + 2ln2) = -33/4
total = simplify(t1 + t2)
expected = Rational(-33, 4)

# t1이 극대(f''<0), t2가 극소(f''>0)인지 확인
fpp = diff(fp, x)
assert fpp.subs(x, Rational(1,2)) < 0, 'x=1/2 should be local max'
assert fpp.subs(x, 2) > 0, 'x=2 should be local min'

if total == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {expected}, got {total}')
