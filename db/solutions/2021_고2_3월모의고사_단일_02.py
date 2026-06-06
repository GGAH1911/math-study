x = -1
y = 2

left = 3*x + (2 + 1j)*y
right = 1 + 2j

if left == right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')