from sympy import symbols, solve, Abs

a1, k = symbols('a1 k', integer=True, positive=True)

# 등차수열: a_n = a1 - 2(n-1)
# a_k = a1 - 2(k-1)

# 주어진 a1=6, k=5
a1_val, k_val = 6, 5

# 조건 1: a1 * a5 <= 0
a5 = a1_val - 2*(5-1)
check1 = a1_val * a5 <= 0

# 조건 2: |a1 - a_k| = 4|a_k|
a_k = a1_val - 2*(k_val-1)
check2 = abs(a1_val - a_k) == 4 * abs(a_k)

if check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')