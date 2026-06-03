import sympy as sp

x = sp.Symbol('x', real=True)
f = 2**(2*x) - 2**(x+2) + 6

# minimum at x=1
f_at_1 = f.subs(x, 1)
# maximum at x=3
f_at_3 = f.subs(x, 3)

# check minimum: derivative = 0 at x=1
df = sp.diff(f, x)
crit = sp.solve(df, x)

print(f'f(1) = {f_at_1}')   # 2
print(f'f(3) = {f_at_3}')   # 38
print(f'critical points: {crit}')  # x=1

total = f_at_1 + f_at_3
if total == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
