z1 = complex(3, 1)
z2 = complex(1, -3)
result = z1 + z2
expected = complex(4, -2)
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')