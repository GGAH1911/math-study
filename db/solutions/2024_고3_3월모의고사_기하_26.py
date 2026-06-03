from sympy import symbols, simplify

# 검증할 네 가지 경우
cases = [(0, 4), (0, -4), (2, 2), (2, -6)]
valid_diff = []

for a, b in cases:
    # 조건 1: 원점을 지나는가?
    origin_check = (0 - a + 1)**2 == (a + b) * 0 + 1
    if not origin_check:
        print('VERIFY_FAIL')
        exit()
    
    # 조건 2: 초점과 준선 사이의 거리 = 2인가?
    p = (a + b) / 4
    distance = abs(2 * p)
    if abs(distance - 2) > 1e-10:
        print('VERIFY_FAIL')
        exit()
    
    valid_diff.append(a - b)

M = max(valid_diff)
m = min(valid_diff)
result = M - m

if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')