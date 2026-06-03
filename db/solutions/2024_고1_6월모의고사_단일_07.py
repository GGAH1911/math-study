import sympy as sp
k = sp.Symbol('k', real=True)
x = sp.Symbol('x')
# 원래 방정식
eq = x**2 - 2*k*x + k**2 + 3*k - 22
# 판별식
discriminant = 4*k**2 - 4*(k**2 + 3*k - 22)
discriminant_simplified = sp.simplify(discriminant)
print(f'Discriminant: {discriminant_simplified}')
# k=8일 때 판별식 확인
disc_at_8 = discriminant_simplified.subs(k, 8)
print(f'Discriminant at k=8: {disc_at_8}')
# k=7일 때 판별식 확인
disc_at_7 = discriminant_simplified.subs(k, 7)
print(f'Discriminant at k=7: {disc_at_7}')
if disc_at_8 < 0 and disc_at_7 >= 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')