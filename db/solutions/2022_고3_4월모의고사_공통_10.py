from sympy import symbols, expand, solve, simplify

t = symbols('t')
a_val = 6  # derived value

# Original velocity
v = 3*(t - 2)*(t - a_val)

# Position from integration with x(0)=0
from sympy import integrate
x = integrate(v, t)  # indefinite, then apply x(0)=0
x = x - x.subs(t, 0)  # ensure x(0)=0

# Check x(0) = 0
assert x.subs(t, 0) == 0, 'x(0) != 0'

# Check that for t > 0, x(t)=0 has exactly one solution
from sympy import solve, S
zeros = solve(x, t)
pos_zeros = [z for z in zeros if z.is_real and z > 0]
assert len(pos_zeros) == 1, f'Expected 1 positive zero, got {pos_zeros}'

# Check a > 2
assert a_val > 2

# Compute v(8)
v8 = v.subs(t, 8)
assert v8 == 36, f'v(8) = {v8}, expected 36'

print('VERIFY_PASS')
