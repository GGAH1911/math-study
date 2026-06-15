from sympy import symbols, limit, Function, simplify
x = symbols('x')
f = Function('f')

# 주어진 조건: lim(x->1) (x-1)f(x) = 3
# 구하는 값: lim(x->1) (x^2-1)f(x)

# (x^2 - 1) = (x - 1)(x + 1)
# lim(x->1) (x^2-1)f(x) = lim(x->1) (x-1)f(x) * (x+1)
# = 3 * 2 = 6

result = 3 * (1 + 1)
print(f'lim(x->1) (x^2-1)f(x) = {result}')

if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')