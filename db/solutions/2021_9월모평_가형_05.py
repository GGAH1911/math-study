import sympy as sp
from sympy import symbols, integrate, Piecewise, sqrt

# 확률밀도함수는 x=4에 대해 대칭
# f(4-t) = f(4+t)
# f는 선형조각함수로 모델링: 0~4에서 증가, 4~8에서 대칭적으로 감소

# f(x) = cx for 0 <= x <= 4
# f(x) = c(8-x) for 4 <= x <= 8
# 이렇게 하면 자동으로 x=4 대칭

c = symbols('c', positive=True, real=True)
x = symbols('x', real=True)

# 확률밀도함수
def f(x_val):
    if isinstance(x_val, (int, float)):
        if 0 <= x_val <= 4:
            return 0.5 * x_val
        else:
            return 0.5 * (8 - x_val)
    else:
        return Piecewise((0.5*x_val, (x_val >= 0) & (x_val <= 4)), (0.5*(8-x_val), (x_val > 4) & (x_val <= 8)))

# 확률밀도함수의 적분 = 1 확인
# ∫[0,4] cx dx + ∫[4,8] c(8-x) dx = 1
# c[x²/2]₀⁴ + c[8x - x²/2]₄⁸ = 1
# c(8) + c(64 - 32 - 32 + 8) = 1
# c(8 + 8) = 16c = 1
# c = 1/16... 다시 계산

# ∫[0,4] cx dx = c·16/2 = 8c
# ∫[4,8] c(8-x) dx = c[8x - x²/2]₄⁸ = c[(64 - 32) - (32 - 8)] = c[32 - 24] = 8c
# 전체 = 16c = 1 ⟹ c = 1/16

# 하지만 우리의 목적: 확률 비율만 확인
# P(2≤X≤4) vs P(6≤X≤8) 비율

# 3P(2≤X≤4) = 4P(6≤X≤8) 확인
# 선형함수로 계산
# P(2≤X≤4) = ∫[2,4] c(x) dx = c∫[2,4] x dx = c[x²/2]₂⁴ = c(8 - 2) = 6c
# P(6≤X≤8) = ∫[6,8] c(8-x) dx = c[8x - x²/2]₆⁸ = c[(64-32) - (48-18)] = c[32 - 30] = 2c

# 확인: 3(6c) = 4(2c) ⟹ 18c = 8c (불만족)
# 다시 설정 필요

# 일반적인 사다리꼴 대칭분포
# P(2≤X≤4) = A, P(6≤X≤8) = B로 설정
# 조건: 3A = 4B
# 대칭성: P(0≤X≤2) = B, P(4≤X≤6) = A
# 전체: 2A + 2B = 1

A_val = 2/7
B_val = 3*A_val/4  # B = 3A/4

# 검증
total = 2*A_val + 2*B_val
condition = 3*A_val - 4*B_val

result = 2*A_val  # P(2≤X≤6)

if abs(total - 1) < 1e-10 and abs(condition) < 1e-10 and abs(result - 4/7) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')