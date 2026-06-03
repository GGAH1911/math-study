# 첫 번째 부등식: 3x >= x - 3
# 두 번째 부등식: 2x + 1 <= 11

integers = []
for x in range(-10, 20):
    if 3*x >= x - 3 and 2*x + 1 <= 11:
        integers.append(x)

total_sum = sum(integers)
expected_answer = 14

if total_sum == expected_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')