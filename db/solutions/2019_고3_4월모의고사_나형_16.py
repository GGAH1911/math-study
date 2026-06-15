from sympy import symbols, solve, log, simplify

a, b = symbols('a b', real=True)

# 주어진 조건: 2^a = 3, 6^b = 5
# a = log_2(3), b = log_6(5)

a_val = log(3, 2)
b_val = log(5, 6)

# 2^(ab+a+b) 계산
result = 2**(a_val*b_val + a_val + b_val)
result_simplified = simplify(result)

print(f'Result: {result_simplified}')
if abs(float(result_simplified) - 15.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')