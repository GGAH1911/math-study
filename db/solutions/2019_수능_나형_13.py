from sympy import Rational, simplify

CANDIDATE = 1

# 보기 (①=30, ②=35, ③=40, ④=45, ⑤=50)
choices = [30, 35, 40, 45, 50]
expected_answer = choices[CANDIDATE - 1]

# 수열의 처음 5항 계산으로 주기성 확인
a1 = Rational(2)
a2 = a1 / (2 - 3*a1)        # n=1 홀수: a2 = 2/(2-6) = -1/2
a3 = 1 + a2                 # n=2 짝수: a3 = 1 + (-1/2) = 1/2
a4 = a3 / (2 - 3*a3)        # n=3 홀수: a4 = (1/2)/(2-3/2) = 1
a5 = 1 + a4                 # n=4 짝수: a5 = 1 + 1 = 2

# 주기성 검증: a5 == a1 이면 주기 4
if a5 == a1:
    # 한 주기의 합
    period_sum = simplify(a1 + a2 + a3 + a4)
    # 전체 합 (40항 = 10주기)
    total_sum = 10 * period_sum
    
    # 정답과 비교
    if total_sum == expected_answer:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")