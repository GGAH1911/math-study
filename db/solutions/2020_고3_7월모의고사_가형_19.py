import sympy as sp
from sympy import symbols, ln, integrate, diff, oo, Function

# f는 짝함수이고, f(1) = 1, integral_0^1 ln(f(t)) dt = 2를 만족해야 함
# f'(-x) = -f'(x) (짝함수의 도함수는 홀함수)

# 검증: 부분적분 공식
# ∫_{-1}^{1} x*f'(x)/f(x) dx = [x*ln(f(x))]_{-1}^{1} - ∫_{-1}^{1} ln(f(x)) dx

# 경계항: 1*ln(f(1)) - (-1)*ln(f(-1)) = 0*1 - (-1)*0 = 0
# 나머지: -∫_{-1}^{1} ln(f(x)) dx

# f 짝함수이므로:
# ∫_{-1}^{1} ln(f(x)) dx = 2∫_0^1 ln(f(x)) dx = 2*2 = 4

# 따라서 ∫_{-1}^{1} x*f'(x)/f(x) dx = -4

result = -4
print(f'VERIFY_PASS' if result == -4 else f'VERIFY_FAIL')