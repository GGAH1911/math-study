import sympy as sp
from sympy import symbols, cos, sin, sqrt, simplify

# Check M^2 + m^2
M_squared = 11 + 2*sqrt(10)
m_squared = sp.Rational(1, 2)

result = M_squared + m_squared
print(f'M^2 + m^2 = {result}')

# Verify form p + 2*sqrt(q)
p_val = sp.Rational(23, 2)
q_val = 10
expected = p_val + 2*sqrt(q_val)

if simplify(result - expected) == 0:
    print(f'p = {p_val}, q = {q_val}')
    print(f'p × q = {p_val * q_val}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')