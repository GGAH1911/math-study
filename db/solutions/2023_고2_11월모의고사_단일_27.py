from sympy import symbols, solve, simplify

# 각 d 값에 대해 검증
results = []
for d in [1, 2, 5, 10]:
    a1 = -3*d - 10
    # a8과 a6 계산
    a8 = a1 + 7*d
    a6 = a1 + 5*d
    # 조건 (가) 확인: a8 = 2*a6 + 10
    if a8 == 2*a6 + 10:
        # a_k = 0인 k 찾기
        k = 4 + 10//d
        a_k = a1 + (k-1)*d
        # 조건 (나) 확인: a_k = 0
        if abs(a_k) < 1e-10:
            results.append(d)

# 최종 답
answer_sum = sum(results)
if answer_sum == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')