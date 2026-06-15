from sympy import symbols, limit, simplify, Poly
x = symbols('x')

# Given conditions
# limit (x+1)*f(x) as x->2 = 6
# limit (x^2+ax-1)*f(x) as x->2 = 26

# Since f is a polynomial and continuous, f(2) exists
# If f(2) ≠ 0, then:
# lim (x+1)*f(x) = (2+1)*f(2) = 3*f(2) = 6
# So f(2) = 2

f_2 = 6 / 3
assert f_2 == 2, f'f(2) should be 2, got {f_2}'

# At x=2: x^2 + ax - 1 = 4 + 2a - 1 = 3 + 2a
# If 3+2a ≠ 0:
# lim (x^2+ax-1)*f(x) = (3+2a)*f(2) = (3+2a)*2 = 26
# So 3+2a = 13, thus a = 5

a = (26/2 - 3) / 2
assert a == 5, f'a should be 5, got {a}'

# Verify conditions
result = a + f_2
print(f'a = {a}, f(2) = {f_2}')
print(f'Condition 1: (2+1)*f(2) = {3*f_2} (should be 6)')
print(f'Condition 2: (4+2*{a}-1)*f(2) = {(4+2*a-1)*f_2} (should be 26)')
print(f'Answer: a + f(2) = {result}')
assert result == 7
print('VERIFY_PASS')