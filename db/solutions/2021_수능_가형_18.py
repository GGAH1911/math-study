from sympy import symbols, limit, oo, simplify, solve, Rational

a, x, n = symbols('a x n', real=True)

# f(x) 정의 (극한)
def f_at_point(x_val, a_val):
    if abs(x_val) < 1:
        return 2 * x_val
    elif x_val == 1:
        return a_val / 4
    elif x_val == -1:
        return -a_val / 4
    else:  # |x_val| > 1
        return (a_val - 2) * x_val / 3

# 두 후보 값 검증
for a_val in [Rational(5, 2), 5]:
    f_1 = f_at_point(1, a_val)
    f_f_1 = f_at_point(float(f_1), a_val)
    if abs(float(f_f_1 - Rational(5, 4))) < 1e-9:
        print(f'a={a_val}: (f∘f)(1)={f_f_1}=5/4 ✓')
    else:
        print(f'a={a_val}: VERIFY_FAIL')
        exit()

# 합 검증
sum_a = Rational(5, 2) + 5
if sum_a == Rational(15, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')