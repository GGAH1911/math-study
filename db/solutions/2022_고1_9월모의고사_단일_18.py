import sympy as sp
k = sp.Symbol('k')
x = sp.Symbol('x')

# 각 k 값에서 판별식 계산
for k_val in range(-5, 10):
    f = x**2 + 4*x - 3*k_val**2 - 12*k_val + 40
    g = x**2 - 12*x + 3*k_val**2 - 36*k_val + 96
    
    disc_f = sp.discriminant(f, x)
    disc_g = sp.discriminant(g, x)
    
    # 부호가 같아야 함 (둘 다 양수, 둘 다 음수, 또는 둘 다 0)
    same_sign = (disc_f * disc_g >= 0)
    if not same_sign:
        print(f'VERIFY_FAIL')
        exit()

count = 0
for k_val in range(-5, 10):
    disc_f = 12*(k_val**2 + 4*k_val - 12)
    disc_g = -12*(k_val**2 - 12*k_val + 20)
    if disc_f * disc_g >= 0:
        count += 1

if count == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')