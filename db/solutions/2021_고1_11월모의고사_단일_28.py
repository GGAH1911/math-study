import sympy as sp

a = sp.Symbol('a', real=True)

# 정의 함수
def f(x):
    if isinstance(x, (int, float)):
        if x < 2:
            return 2*x + 2
        else:
            return x**2 - 7*x + 16
    else:
        # symbolic
        return sp.Piecewise((2*x + 2, x < 2), (x**2 - 7*x + 16, True))

# 검증: a = -2, 1, 3, 4
test_values = [-2, 1, 3, 4]
all_pass = True

for val in test_values:
    f_a = f(val)
    f_f_a = f(f_a)
    if f_f_a == f_a:
        pass
    else:
        all_pass = False
        break

# 합 검증
total_sum = sum(test_values)
if total_sum == 6 and all_pass:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')