from math import comb
from sympy import binomial, simplify

# 원래 식 그대로 코드화: sum of C(4,k) * 3^k for k=0..4
original_expression = sum(comb(4, k) * (3 ** k) for k in range(5))

# 이항정리 풀이: (1+3)^4 = 4^4
binomial_theorem_result = (1 + 3) ** 4

# sympy로 정확하게 검증
sympy_result = sum(binomial(4, k) * 3**k for k in range(5))
sympy_simplified = simplify(sympy_result)

# 각 항 상세 계산
term_0 = comb(4, 0) * (3 ** 0)  # 1 * 1 = 1
term_1 = comb(4, 1) * (3 ** 1)  # 4 * 3 = 12
term_2 = comb(4, 2) * (3 ** 2)  # 6 * 9 = 54
term_3 = comb(4, 3) * (3 ** 3)  # 4 * 27 = 108
term_4 = comb(4, 4) * (3 ** 4)  # 1 * 81 = 81

direct_sum = term_0 + term_1 + term_2 + term_3 + term_4

# 예상되는 답: 4^4 = 256
expected_answer = 256

# 모든 계산이 일치하는지 확인
assert original_expression == expected_answer, f"Original: {original_expression} != {expected_answer}"
assert binomial_theorem_result == expected_answer, f"Binomial: {binomial_theorem_result} != {expected_answer}"
assert sympy_simplified == expected_answer, f"SymPy: {sympy_simplified} != {expected_answer}"
assert direct_sum == expected_answer, f"Direct sum: {direct_sum} != {expected_answer}"

# 최종 검증: 원래 식이 조건을 만족하는가?
if original_expression == expected_answer and sympy_simplified == expected_answer:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")