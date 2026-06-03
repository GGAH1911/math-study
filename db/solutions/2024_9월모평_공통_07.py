import math

# Given conditions
# 3a + 2b = log_3(32)
# ab = log_9(2)

log3_2 = math.log(2) / math.log(3)
condition1 = 5 * log3_2  # log_3(32) = log_3(2^5) = 5*log_3(2)
condition2 = log3_2 / 2  # log_9(2) = log_3(2)/2

# Our answer
answer = 5/3

# Verify: (1/(3a) + 1/(2b)) should equal answer
# Which is equivalent to: (3a + 2b) / (6ab) = answer
computed = condition1 / (6 * condition2)

if abs(computed - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')