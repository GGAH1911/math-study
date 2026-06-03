from sympy import symbols, sqrt, limit, oo, simplify

n, a1, d = symbols('n a1 d', real=True, positive=True)
an = a1 + (n-1)*d

expr = sqrt(an**2 + 2*n) - an
lim_val = limit(expr, n, oo)

print(f'극한값 (d 기호): {lim_val}')
print(f'극한값 단순화: {simplify(lim_val)}')

# d=3일 때 검증
d_val = 3
lim_result = lim_val.subs(d, d_val)
print(f'd=3일 때 극한값: {lim_result}')
print(f'목표값 1/3과 비교: {float(lim_result)}')

if abs(float(lim_result) - 1/3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')