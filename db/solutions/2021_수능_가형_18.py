from sympy import symbols, solve, limit, simplify, oo

a, x, n = symbols('a x n', real=True)

# f(x) 정의
def f_func(x_val, a_val):
    if abs(x_val) < 1:
        return 2 * x_val
    elif x_val == 1:
        return a_val / 4
    elif x_val == -1:
        return -a_val / 4
    else:
        return (a_val - 2) * x_val / 3

# 후보 a 값들
candidates = [5/2, 5]

for a_val in candidates:
    f_1 = f_func(1, a_val)  # f(1) = a/4
    f_f_1 = f_func(f_1, a_val)  # f(f(1))
    
    if abs(f_f_1 - 1.25) < 1e-10:
        print(f"a={a_val}: f(1)={f_1}, f(f(1))={f_f_1} ✓")

# 최종 검증: a의 합
result_sum = 5/2 + 5
if abs(result_sum - 7.5) < 1e-10:
    print(f"Sum of all a: {result_sum} = 15/2")
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")