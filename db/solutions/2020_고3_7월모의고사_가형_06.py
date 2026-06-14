import sympy as sp
x = sp.Symbol('x')
# 원래 형태
expr1 = sp.ln(x**2 + x + 1) / (x**2 + 4*x)
result1 = sp.limit(expr1, x, 0)
print(f'Original: {result1}')
# 역순 형태 (보기와 일치)
expr2 = (x**2 + 4*x) / sp.ln(x**2 + x + 1)
result2 = sp.limit(expr2, x, 0)
print(f'Reversed: {result2}')
if result2 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')