from sympy import symbols, exp, diff, simplify, solve, Rational, sqrt, E
t, k = symbols('t k', positive=True, real=True)
# f(t) = AC/AB = t / (a^{2t} * ln(a)) = t*exp(-2*k*t)/k  where k=ln(a)
f = t * exp(-2 * k * t) / k
df = diff(f, t)
# critical point: t = 1/(2k)
critical = solve(df, t)  # [1/(2k)]
# for max at t=1: 1/(2k)=1 => k=1/2
k_val = Rational(1, 2)
f_sub = f.subs(k, k_val)    # 2t*exp(-t)
df_sub = diff(f_sub, t)      # 2*(1-t)*exp(-t)
d2f_sub = diff(f_sub, t, 2)  # 2*(t-2)*exp(-t)
df_at_1  = simplify(df_sub.subs(t, 1))
d2f_at_1 = simplify(d2f_sub.subs(t, 1))
crit_sub = solve(df_sub, t)  # [1]
PASS = (df_at_1 == 0) and (d2f_at_1 < 0) and (crit_sub == [1])
print('VERIFY_PASS' if PASS else 'VERIFY_FAIL')