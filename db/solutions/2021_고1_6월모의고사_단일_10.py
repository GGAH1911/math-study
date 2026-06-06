import sympy as sp
k = sp.Symbol('k')
x = sp.Symbol('x')

# 방정식: x^2 + 6x - 3 = kx - 7
# 정리: x^2 + (6-k)x + 4 = 0

eq = x**2 + (6-k)*x + 4

# k = 3, 4, 5, 6, 7, 8, 9에서 판별식 < 0 확인
valid_count = 0
for k_val in range(1, 12):
    discriminant = (6 - k_val)**2 - 4*1*4
    if discriminant < 0:
        valid_count += 1
        
if valid_count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')