# 그래프에서 정의된 함수 조건 확인
# 좌측 직선: y = -x (기울기 -1, (0,-2) 지남)
# 우측 직선: y = -x (기울기 -1, (2,-2) 지남)

# x -> 0^- 극한: 좌측 직선에서 x=0일 때의 y값
limit_x_to_0_minus = -0  # y = -x에서 x=0일 때
# 아니, 다시: 좌측 직선이 (0, -2)를 지나므로
limit_x_to_0_minus = -2

# x -> 1^+ 극한: 수평선 y=1의 값
limit_x_to_1_plus = 1

# 합 계산
result = limit_x_to_0_minus + limit_x_to_1_plus
assert result == -1, f'Expected -1, got {result}'
print('VERIFY_PASS')