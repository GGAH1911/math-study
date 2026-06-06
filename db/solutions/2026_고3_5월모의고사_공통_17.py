# 조건: sum(a_{2k}) = sum(k^2 - a_{2k-1})
# 우변 전개: sum(a_{2k}) = sum(k^2) - sum(a_{2k-1})
# 정리: sum(a_{2k}) + sum(a_{2k-1}) = sum(k^2)
# 즉, sum(a_1...a_14) = sum(k^2 for k=1..7)

sum_of_squares = sum(k**2 for k in range(1, 8))
expected = sum_of_squares

if expected == 140:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')