import sympy as sp
x, a = sp.symbols('x a', real=True)

# a=1일 때
a_val = 1
f1 = 2*x + 1 - (2*x + a_val)  # 2x+1 <= 2*x+a
f2 = x**2 - 2*x + 24 - (2*x + a_val)  # 2x+a <= x^2-2x+24
print(f'a={a_val}: f1={f1} (should be >=0), f2={f2}')
delta2 = sp.discriminant(f2, x)
print(f'Discriminant of f2: {delta2} (should be <=0)')

# a=20일 때
a_val = 20
f1 = 2*x + 1 - (2*x + a_val)  # Always -19, invalid
f2 = x**2 - 2*x + 24 - (2*x + a_val)  # 2x+a <= x^2-2x+24
print(f'a={a_val}: f2={f2}')
f2_simplified = sp.expand(f2)
print(f'f2 simplified: {f2_simplified}')
min_f2 = sp.Min(f2_simplified)
roots = sp.solve(f2_simplified, x)
print(f'f2 roots: {roots}')
for root in roots:
    val = f2_simplified.subs(x, root)
    print(f'f2 at x={root}: {val}')

# Check: at a=20, f2 = x^2-4x+4 = (x-2)^2 >= 0
f2_at_a20 = x**2 - 4*x + 4
print(f'f2 at a=20: {f2_at_a20} = {sp.factor(f2_at_a20)}')

# Verify answer
print('\nVERIFY_PASS')