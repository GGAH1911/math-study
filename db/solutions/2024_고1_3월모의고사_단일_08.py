from itertools import product

# 두 주사위 (a, b)의 모든 가능한 경우
all_outcomes = list(product(range(1, 7), repeat=2))

# 차가 2 또는 4인 경우만 필터링
satisfying = [outcome for outcome in all_outcomes if abs(outcome[0] - outcome[1]) == 2 or abs(outcome[0] - outcome[1]) == 4]

# 확률 계산
prob = len(satisfying) / len(all_outcomes)
expected = 1/3

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')