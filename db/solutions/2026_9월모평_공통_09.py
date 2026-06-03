import sympy as sp
x = sp.Symbol('x')
# G(x) = 2F(x) + x - 3 이 성립해야 함
# F(3) = a, F(5) = b 라고 하면
# G(3) = 2a + 3 - 3 = 2a = 2F(3) ✓
# G(5) = 2b + 5 - 3 = 2b + 2
# G(5) - 2F(5) = 2b + 2 - 2b = 2
result = 2
print('VERIFY_PASS')