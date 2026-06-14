from math import factorial

CANDIDATE = 840

# 번사이드 보조정리를 이용한 검증
# 7개 원의 배치: 중앙 1개 + 주변 6개 (6-fold 회전 대칭)

# 회전군: {0°, 60°, 120°, 180°, 240°, 300°}
rotations = [0, 60, 120, 180, 240, 300]
group_size = len(rotations)

# 각 회전에 대한 고정점 개수 계산
fixed_count = {}

# 항등원 (0도): 모든 7! 색칠이 불변
fixed_count[0] = factorial(7)

# 60도 회전: 중앙 고정, 바깥 6개가 하나의 6-사이클
# 7개 서로 다른 색을 모두 사용하므로 6-사이클이 모두 같은 색일 수 없음
fixed_count[60] = 0

# 120도 회전: 중앙 고정, 바깥 6개가 두 개의 3-사이클
# 각 3-사이클이 불변이려면 같은 색이어야 하는데, 7개 색을 모두 써야 하므로 불가능
fixed_count[120] = 0

# 180도 회전: 중앙 고정, 바깥 6개가 세 개의 2-사이클
# 각 2-사이클이 불변이려면 같은 색이어야 하는데, 7개 색을 모두 써야 하므로 불가능
fixed_count[180] = 0

# 240도, 300도: 마찬가지로 0
fixed_count[240] = 0
fixed_count[300] = 0

# 번사이드 보조정리
total_fixed = sum(fixed_count.values())
result = total_fixed // group_size

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')