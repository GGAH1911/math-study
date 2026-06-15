import sympy as sp

CANDIDATE = 15

x = sp.Symbol('x')
f = -sp.Rational(1,4) * x**2 + sp.Rational(7,4) * x

# 자연수 검증
natural_numbers = []
for n in range(1, 8):
    if n == 1 or n == 7:
        continue  # 경계값
    try:
        f_val = float(f.subs(x, n))
        x_minus_1 = n - 1
        # f(x) > 0 and x > 1 and f(x) <= x-1
        if f_val > 0 and n > 1 and f_val <= x_minus_1:
            natural_numbers.append(n)
    except:
        pass

computed_sum = sum(natural_numbers)

if computed_sum == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')