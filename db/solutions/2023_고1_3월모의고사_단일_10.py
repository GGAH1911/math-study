def f(x):
    return x**2 - 3*x + 2

a = 4
b = f(a)

# O(0,0), B(0,2), A(a,b)
# 삼각형 넓이 = |x_A * (y_B - y_O)| / 2 * 2 = a
area = a

if area == 4 and b == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')