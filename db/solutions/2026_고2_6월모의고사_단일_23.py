import math

# 원래 방정식: 5^(x+4) = 25^(2x-4)
x = 4

left = 5**(x+4)
right = 25**(2*x-4)

if math.isclose(left, right, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')