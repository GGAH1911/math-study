from sympy import cbrt, simplify

CANDIDATE = 81

# 원래 문제 식: ³√(27²) × 3²
# 27 = 3³ 이므로 27² = (3³)² = 3⁶
# ³√(27²) = ³√(3⁶) = 3^(6/3) = 3² = 9
# 3² = 9
# 따라서 ³√(27²) × 3² = 9 × 9 = 81

# 주어진 식을 코드로 인코딩
cube_root_27_squared = cbrt(27**2)
three_squared = 3**2
result = cube_root_27_squared * three_squared

# 간단히 정리
result_simplified = simplify(result)

# CANDIDATE와 원래 식의 계산 결과를 비교하여 검증
if result_simplified == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")