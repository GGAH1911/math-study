from sympy import symbols, sqrt, simplify, Eq
a = symbols('a', positive=True)
# 쌍곡선: y²/a² - x²/a² = 1, 점 (a, √2·a) 위의 접선: x - √2·y + a = 0
# y축 교점: P = (0, a√2/2)
# 초점: F = (0, a√2), F' = (0, -a√2)
P_y = a * sqrt(2) / 2
F_y = a * sqrt(2)
F_prime_y = -a * sqrt(2)
PF = abs(F_y - P_y)
PF_prime = abs(F_prime_y - P_y)
product = simplify(PF * PF_prime)
result = simplify(product - 8)
if result == 0:
    print('VERIFY_PASS')
else:
    # a = 4√3/3로 검증
    a_val = 4*sqrt(3)/3
    P_y_val = a_val * sqrt(2) / 2
    F_y_val = a_val * sqrt(2)
    F_prime_y_val = -a_val * sqrt(2)
    PF_val = abs(F_y_val - P_y_val)
    PF_prime_val = abs(F_prime_y_val - P_y_val)
    product_val = simplify(PF_val * PF_prime_val)
    if simplify(product_val - 8) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')