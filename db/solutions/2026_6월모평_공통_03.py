# Given condition: sum(a_k) for k=1 to 7 equals 8
sum_a = 8

# Calculate sum(2*a_k + 1) for k=1 to 7
# = 2*sum(a_k) + 7
result = 2 * sum_a + 7

if result == 23:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')