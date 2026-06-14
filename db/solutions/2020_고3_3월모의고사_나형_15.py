import math

a_1 = 2
a_2 = 1 * a_1

def compute_a(n):
    if n == 1:
        return 2
    elif n >= 2:
        return math.factorial(n)

result = a_2 + compute_a(51) / compute_a(50)
if result == 53:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')