from sympy import Eq, simplify

CANDIDATE = 2  # 보기 번호 (정답)

# 보기 옵션
options = [16, 20, 24, 28, 32]  # ① ② ③ ④ ⑤

# 핵심 관계식:
# 조건 (나): 십의 자리는 6의 약수 → {1, 2, 3, 6} = 4가지
# 조건 (가): 일의 자리는 2의 배수 → {0, 2, 4, 6, 8} = 5가지
# 곱의 법칙: 4 × 5 = 20

tens_divisors_of_6 = 4
ones_even_digits = 5
total_count = tens_divisors_of_6 * ones_even_digits

# CANDIDATE (보기 번호)에 해당하는 옵션값
expected_answer = options[CANDIDATE - 1]

# 수식 관계로 검증
equation = Eq(total_count, expected_answer)
verification = simplify(equation)

if verification == True:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")