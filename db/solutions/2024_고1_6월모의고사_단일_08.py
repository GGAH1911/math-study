from sympy import symbols, mod_inverse

# 2024^4 + 2024^2 + 1을 2022로 나눈 나머지
result = (2024**4 + 2024**2 + 1) % 2022

if result == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')