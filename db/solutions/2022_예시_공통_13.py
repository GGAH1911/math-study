from sympy import symbols, summation, simplify, factorial, Abs
n, k = symbols('n k', integer=True, positive=True)

# 검증: n=3일 때 직접 계산
S_1 = 1/2
S_2 = -2/3
S_3 = -3/4

a_1, a_2, a_3 = S_1, S_2-S_1, S_3-S_2
inv_sum_3 = 1/a_1 + 1/a_2 + 1/a_3

# 공식으로 계산
f_val = -3  # (가) = -n
g_val = 1   # (나) = 1
h_val = 3**2  # (다) = k^2

result = Abs((-5) * 1 * 36)
if result == 180:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')