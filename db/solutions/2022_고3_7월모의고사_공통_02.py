a2 = 1/2
a3 = 1
r = a3 / a2  # 공비 = 2
a5 = a2 * (r ** 3)  # a2 * r^(5-2)
my_answer = 4
print('VERIFY_PASS' if abs(a5 - my_answer) < 1e-9 else 'VERIFY_FAIL')