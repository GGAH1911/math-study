# 직육면체 길이, 너비, 높이
a, b, c = 4, 6, 5

# 조건 검증
assert 4*(a+b+c) == 60, f"모서리 합 검증 실패"
assert 2*(a*b + b*c + c*a) == 148, f"겉넓이 검증 실패"

# 좌표
B = (0, 0, 0)
G = (0, b, c)
D = (a, b, 0)

# 거리 제곱
BG_sq = G[0]**2 + G[1]**2 + G[2]**2
GD_sq = (D[0]-G[0])**2 + (D[1]-G[1])**2 + (D[2]-G[2])**2
DB_sq = D[0]**2 + D[1]**2 + D[2]**2

result = BG_sq + GD_sq + DB_sq

if result == 154:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')