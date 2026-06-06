from sympy import symbols, div, expand, simplify
x = symbols('x')
f = x**3 + 2
divisor = (x + 1) * (x - 2)
q, r = div(f, divisor, x)
remainder = r
print('나머지:', remainder)
a_val = 3
b_val = 4
remainder_check = a_val * x + b_val
if simplify(remainder - remainder_check) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')