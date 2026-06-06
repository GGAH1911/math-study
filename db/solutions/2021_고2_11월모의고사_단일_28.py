from sympy import symbols, limit, diff, factor, simplify, oo
x = symbols('x')
f = 3 * (x - 1) * (x - 2)**2
f_prime = diff(f, x)

limit_ga = limit(f / (x - 1), x, 1)
print(f'조건 (가): {limit_ga} == 3: {limit_ga == 3}')

limit_na = limit(f / ((x - 2) * f_prime), x, 2)
alpha = limit_na
print(f'조건 (나): {limit_na} == 1/2: {limit_na == 1/2}')
print(f'alpha: {alpha}')

f_4 = f.subs(x, 4)
result = alpha * f_4
print(f'f(4): {f_4}')
print(f'alpha × f(4): {result}')

if result == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')