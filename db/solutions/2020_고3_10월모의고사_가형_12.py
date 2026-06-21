import sympy as sp
from sympy import exp, ln, integrate, symbols, simplify, E

t = symbols('t', positive=True, real=True)
a = 1

# f(x) = 2*e^x * (x*e^x + 1) * (x + 1)
x = symbols('x', real=True)
f = 2*exp(x)*(x*exp(x) + a)*(x + 1)

# 검증: 적분 계산
integral_result = integrate(f, (x, 0, ln(t)))
rhs = (t*ln(t) + a)**2 - a

# 우변 전개
rhs_expanded = simplify(rhs)
integral_simplified = simplify(integral_result)

# 두 값이 같은지 확인
if simplify(integral_simplified - rhs_expanded) == 0:
    # f(1) 계산
    f_at_1 = f.subs(x, 1)
    answer = simplify(f_at_1)
    expected = 4*E**2 + 4*E
    if simplify(answer - expected) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')