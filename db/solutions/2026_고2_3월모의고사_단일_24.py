import sympy as sp

# 원래 문제: x^2 - ax + 13 = 0의 근 α, β에 대해
# 조건: 1/α + 1/β = 2

a = 26

# 근과 계수의 관계
# α + β = a = 26
# α·β = 13

# 검증: 1/α + 1/β = (α+β)/(α·β) = a/13
verify = a / 13

if abs(verify - 2.0) < 1e-10:
    # 판별식 확인 (서로 다른 두 근)
    discriminant = a**2 - 4*13
    if discriminant > 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')