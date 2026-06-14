from sympy import symbols, diff, solve, simplify, expand
a = symbols('a', real=True)
f = lambda x: x*(x-a)*(x-6)
f_prime = lambda x: diff(f(x), x)
g = lambda a_val: -3*a_val*(a_val-6)**2/2
g_prime = lambda a_val: diff(g(a_val), a_val)
a_critical = solve(g_prime(a), a)
a_val = 2
m1 = 6*a_val
m2 = -(a_val-6)**2/4
product = m1 * m2
print(f'a={a_val}: m1={m1}, m2={m2}, product={product}')
if product == -48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')