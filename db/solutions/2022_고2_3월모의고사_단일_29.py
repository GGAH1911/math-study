from sympy import symbols, expand, factor, div
x, b = symbols('x b')
# b=1 일 때
g = x + 1
f = x**3 + 3*x**2 + 5*x + 3
# 조건 (가) 검증
quotient, remainder = div(f, x**2 + g, domain='ZZ')
expected_remainder = g**2 - x**2
print('조건 (가) quotient:', quotient, '== x+2:', quotient == x+2)
print('조건 (가) remainder:', expand(remainder), '== g^2-x^2:', expand(remainder) == expand(expected_remainder))
# 조건 (나) 검증
quotient2, remainder2 = div(f, g, domain='ZZ')
print('조건 (나) remainder:', remainder2, '== 0:', remainder2 == 0)
# f(0) != 0 검증
print('f(0) =', f.subs(x, 0), '!= 0:', f.subs(x, 0) != 0)
# 답 계산
ans = f.subs(x, 2)
print('f(2) =', ans, '== 33:', ans == 33)
if ans == 33:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')