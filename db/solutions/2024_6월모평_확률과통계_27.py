from itertools import product

# 주사위 두 번: a, b ∈ {1,2,3,4,5,6}
cases = [(a, b) for a in range(1, 7) for b in range(1, 7)]

# a×b가 4의 배수인 경우
multiple_of_4 = [(a, b) for a, b in cases if (a * b) % 4 == 0]

# a+b ≤ 7이면서 a×b가 4의 배수
both_conditions = [(a, b) for a, b in multiple_of_4 if a + b <= 7]

# 확률
prob = len(both_conditions) / len(multiple_of_4)

# 7/15와 비교
expected = 7 / 15

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')