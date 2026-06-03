from sympy import symbols, Abs, solve, summation

n, k = symbols('n k', integer=True)
a1, d = -13, 4

# 등차수열 정의
def a(n_val):
    return a1 + (n_val - 1) * d

# 조건 (가) 검증: |a_4| + |a_6| = 8
cond_ga = abs(a(4)) + abs(a(6))
assert cond_ga == 8, f'조건 (가) 실패: {cond_ga}'

# 조건 (나) 검증: sum(a_k, k=1~9) = 27
cond_na = sum(a(i) for i in range(1, 10))
assert cond_na == 27, f'조건 (나) 실패: {cond_na}'

# 답: a_10
answer = a(10)
assert answer == 23, f'a_10 = {answer}'

print('VERIFY_PASS')