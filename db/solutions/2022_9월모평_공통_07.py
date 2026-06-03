import sympy as sp
from sympy import symbols, summation, simplify

# 공식 검증
n = symbols('n', positive=True, integer=True)
a_n1 = -4*n/(n+4)  # a_{n+1}의 일반식

# n=1일 때 a_2 확인
a_2 = a_n1.subs(n, 1)
print(f'a_2 = {a_2}')  # -4/5

# 텔레스코핑 급수 검증: sum = 1/a_1 - 1/a_{n+1} = 1/n이어야 함
# 1/(-4) - 1/a_{n+1} = 1/n
# -1/4 - 1/(-4n/(n+4)) = 1/n
# -1/4 + (n+4)/(4n) = 1/n
lhs = -sp.Rational(1,4) + (n+4)/(4*n)
rhs = 1/n
verify_condition = simplify(lhs - rhs)
print(f'Condition check (should be 0): {verify_condition}')

# a_13 계산
a_13 = a_n1.subs(n, 12)
print(f'a_13 = {a_13}')

if a_13 == -3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')