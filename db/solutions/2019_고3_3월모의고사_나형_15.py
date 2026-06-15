from sympy import symbols, solve, Abs

def count_real_cube_roots(a):
    """x^3 = a의 실근 개수"""
    return 1

def count_real_fourth_roots(a):
    """x^4 = a의 실근 개수"""
    if a > 0:
        return 2
    elif a == 0:
        return 1
    else:
        return 0

def f(n):
    return count_real_cube_roots(n * (n - 4))

def g(n):
    return count_real_fourth_roots(n * (n - 4))

# f(n) > g(n)을 만족하는 모든 자연수 n 찾기
valid_n = []
for n in range(1, 50):
    if f(n) > g(n):
        valid_n.append(n)

result_sum = sum(valid_n)

# 검증
assert valid_n == [1, 2, 3], f"Expected [1, 2, 3], got {valid_n}"
assert result_sum == 6, f"Expected 6, got {result_sum}"

print('VERIFY_PASS')