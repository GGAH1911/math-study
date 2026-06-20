import sympy as sp
valid_m = []
prod = sp.Integer(1)
for m in range(1, 600):
    prod *= sp.Rational(2*(m+1), m+2)
    s = sp.simplify(sp.log(sp.sqrt(prod), 2))
    if s.is_integer and 1 <= int(s) <= 100:
        valid_m.append(m)
answer = sum(valid_m)
print('valid m:', valid_m, 'sum:', answer)
print('VERIFY_PASS' if (answer == 162 and valid_m == [6, 30, 126]) else 'VERIFY_FAIL')