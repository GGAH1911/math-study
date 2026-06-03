from sympy import symbols, expand, simplify

n = 2023
numerator = 2022 * (2023**2 + 2024)
denominator = 2024 * 2023 + 1
result = numerator / denominator

if abs(result - 2022) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')