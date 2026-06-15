from sympy import symbols, solve, simplify
x, a = symbols('x a', real=True)
# 명제가 참 ⟹ x=2일 때 x^2 - ax + a = 0 성립
eq = x**2 - a*x + a
result = eq.subs(x, 2)
a_val = solve(result, a)[0]
print(f'a = {a_val}')
# 검증: a=4일 때 x=2이 방정식의 해인지 확인
eq_check = x**2 - 4*x + 4
check = eq_check.subs(x, 2)
if simplify(check) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')