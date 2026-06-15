a = (3, -2)
b = (2, -6)
diff = (a[0] - b[0], a[1] - b[1])
component_sum = diff[0] + diff[1]
if component_sum == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')