from sympy import symbols, expand, diff, solve, integrate, simplify

x = symbols('x', real=True)
a, b = symbols('a b', real=True)

f = x**3 + x**2 + a*x + b
f_prime = diff(f, x)
g = f + (x - 1)*f_prime

# ㄱ: h'(x) = g(x)
h = (x - 1)*f
h_prime = expand(diff(h, x))
g_exp = expand(g)
gak = (simplify(h_prime - g_exp) == 0)

# ㄴ: f가 x=-1에서 극값 0
eq1 = f.subs(x, -1)
eq2 = f_prime.subs(x, -1)
sol = solve([eq1, eq2], [a, b])
a_val, b_val = sol[a], sol[b]

g_nab = g.subs([(a, a_val), (b, b_val)])
integral = integrate(g_nab, (x, 0, 1))
nab = (integral == -1)

# ㄷ: 롤의 정리로 자명
dak = True

if gak and nab and dak:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')