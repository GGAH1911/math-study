import sympy as sp
a, b = -2, 1
R = lambda x: a * x + b
result_at_minus1 = R(-1)
result_at_2 = R(2)
assert result_at_minus1 == 3, f'R(-1) = {result_at_minus1}, expected 3'
assert result_at_2 == -3, f'R(2) = {result_at_2}, expected -3'
result = R(3)
assert result == -5, f'R(3) = {result}, expected -5'
print('VERIFY_PASS')