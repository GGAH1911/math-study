import sympy as sp

# 조건 p: x = 3만 만족
p_set = {3}

# 조건 q를 정리: |x - a| <= 2는 a - 2 <= x <= a + 2
# p가 q의 충분조건이려면 p ⊆ q
# 즉, 3이 [a-2, a+2]에 포함되어야 함

def check_condition(a):
    """a가 조건을 만족하는지 확인"""
    lower = a - 2
    upper = a + 2
    return lower <= 3 <= upper

# 최솟값과 최댓값 찾기
# a - 2 <= 3 <= a + 2에서:
# a <= 5 and a >= 1

a_min = 1
a_max = 5

# 검증
assert check_condition(a_min), f"a_min = {a_min} 실패"
assert check_condition(a_max), f"a_max = {a_max} 실패"

# 경계 외 확인
assert not check_condition(0.99), "a < 1 범위 확인"
assert not check_condition(5.01), "a > 5 범위 확인"

# 답 검증
answer_sum = a_max + a_min
assert answer_sum == 6, f"합이 6이 아님: {answer_sum}"

print('VERIFY_PASS')