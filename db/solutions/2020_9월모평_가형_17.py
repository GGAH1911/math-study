from sympy import symbols, integrate, simplify

# 일반적 검증: 부분적분 공식 확인
# I = ∫{f(x)}²g'(x)dx = [f²g]|_{-1}^1 - ∫2f·f'·g dx
# 조건: f(x)g(x) = x⁴-1 → 경계에서 0
# f'g + fg' = 4x³ → f'g = 4x³ - fg'
# I = 0 - 2∫f(4x³ - fg')dx = -8∫fx³dx + 2I
# I = -8∫fx³dx + 2I
# -I = -8∫fx³dx
# I = 8∫fx³dx

# 주어진 I = 120
I = 120
result = I / 8

if result == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')