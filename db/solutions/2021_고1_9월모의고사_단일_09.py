# 검증: a=2, b=-1이 조건을 만족하는지 확인
# 점 (1, a) = (1, 2)
point = (1, 2)

# y=x에 대해 대칭이동
A = (point[1], point[0])
assert A == (2, 1), f"A should be (2, 1), got {A}"

# A를 x축에 대해 대칭이동
final_point = (A[0], -A[1])
assert final_point == (2, -1), f"Final point should be (2, -1), got {final_point}"

# 조건 확인: b = -1
b = -1
a = 2
result = a + b
assert result == 1, f"a + b should be 1, got {result}"

print('VERIFY_PASS')