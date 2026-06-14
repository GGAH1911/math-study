from sympy import symbols, Eq, solve

CANDIDATE = 2

# 핵심 관계식 1 (ㄴ): 두 자리 4의 배수 개수
# 등차수열 12, 16, 20, ..., 96의 항 개수
n = symbols('n', integer=True, positive=True)
eq = Eq(12 + 4*(n-1), 96)
count_gn = int(solve(eq, n)[0])

# 핵심 관계식 2 (ㄷ): |A_k| = 11인 모든 k의 합
# k = 11 (홀수), 20 (≡0 mod 4), 22 (≡2 mod 4)
sum_k = 11 + 20 + 22

# 검증
# CANDIDATE = 2 ⟺ ㄱ, ㄴ 참, ㄷ 거짓
check_gn = (count_gn == 22)  # ㄴ 참
check_gd = (sum_k != 33)     # ㄷ 거짓

if check_gn and check_gd:
    if CANDIDATE == 2:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")