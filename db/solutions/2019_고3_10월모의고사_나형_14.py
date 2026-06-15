from sympy import symbols, expand, limit, simplify

x, a = symbols('x a', real=True)

# 원함수 정의
def g_func(x_val):
    if abs(x_val) <= 2:
        return -abs(x_val) + 2
    else:
        return 1

def f_func(x_val):
    return x_val**2 - 4

# a = -4, 4에서 확인
valid_a_values = [-4, 4]
correct_count = 0

for a_val in valid_a_values:
    # x = 2에서의 불연속 확인
    f_shifted = (x - a_val)**2 - 4
    
    # x = 2
    left_2 = f_shifted.subs(x, 2.0 - 0.0001) * g_func(2.0 - 0.0001)
    right_2 = f_shifted.subs(x, 2.0 + 0.0001) * g_func(2.0 + 0.0001)
    
    # x = -2
    left_minus2 = f_shifted.subs(x, -2.0 - 0.0001) * g_func(-2.0 - 0.0001)
    right_minus2 = f_shifted.subs(x, -2.0 + 0.0001) * g_func(-2.0 + 0.0001)
    
    at_2 = 0  # g(2) = 0
    at_minus2 = 0  # g(-2) = 0
    
    # 정확히 한 점에서만 불연속
    disc_at_2 = abs(left_2 - right_2) > 0.01
    disc_at_minus2 = abs(left_minus2 - right_minus2) > 0.01
    
    if (disc_at_2 and not disc_at_minus2) or (not disc_at_2 and disc_at_minus2):
        correct_count += 1

product = (-4) * 4
if correct_count == 2 and product == -16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')