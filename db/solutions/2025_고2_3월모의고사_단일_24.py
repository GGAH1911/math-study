from sympy import symbols, I, expand, solve

# 원래 방정식의 근이 2 + 3i임을 확인
x = symbols('x')
a, b = -4, 13
eq = x**2 + a*x + b

# x = 2 + 3i를 방정식에 대입
result = eq.subs(x, 2 + 3*I)
result_simplified = expand(result)

if result_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Result: {result_simplified}')