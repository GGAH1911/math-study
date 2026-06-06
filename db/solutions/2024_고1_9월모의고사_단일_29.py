from sympy import symbols, solve

# 원래 함수와 구한 값
p, q = 2, 3
m = 3
f = lambda x: (x - p)**2 + q

# 조건 (가) 검증: [0, 3]
vals_a = [f(0), f(3), f(p)]
min_a = min(vals_a)
max_a = max(vals_a)
assert min_a == m, f'조건(가) 최솟값: {min_a} != {m}'
assert max_a == m + 4, f'조건(가) 최댓값: {max_a} != {m+4}'

# 조건 (나) 검증: [0, 5]
vals_b = [f(0), f(5), f(p)]
min_b = min(vals_b)
max_b = max(vals_b)
assert min_b == m, f'조건(나) 최솟값: {min_b} != {m}'
assert max_b == 4*m, f'조건(나) 최댓값: {max_b} != {4*m}'

# f(10) 계산
result = f(10)
assert result == 67, f'f(10) = {result} != 67'

print('VERIFY_PASS')