from sympy import symbols, Abs, limit, simplify

x = symbols('x')

# Define f(x)
def f(val):
    if val < -1:
        return val + 2
    elif -1 <= val < 1:
        return val
    else:  # x >= 1
        return 2 - val

# Define g(x) 
def g(val):
    if -1 <= val <= 1:
        return 1 - abs(val)
    return None

# Check ㄴ: f(1)*g(1) = 0
f_1 = f(1)
g_1 = g(1)
result_n = f_1 * g_1

if result_n == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')