from math import factorial

CANDIDATE = 450

# 경우 1: 홀수 3개를 1번씩, 짝수 1개를 2번씩
# 다중집합 {1, 3, 5, e, e}의 배열: 5! / 2!
case1 = 3 * (factorial(5) // factorial(2))

# 경우 2: 홀수 1개를 1번씩, 짝수 2개를 2번씩
# 다중집합 {o, e1, e1, e2, e2}의 배열: 5! / (2! × 2!)
case2 = 3 * 3 * (factorial(5) // (factorial(2) * factorial(2)))

result = case1 + case2

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {CANDIDATE}, got {result}")