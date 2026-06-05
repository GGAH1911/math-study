from sympy import log, N

a = -5
count_valid = 0

# Part 1: x < 3, f(x) = 2^x
for n in range(1, 8):
    x_sol = log(n, 2)
    if x_sol < 3:
        count_valid += 1

# Part 2: x >= 3
# f(x) = (1/4)^(x-5) - 16 + 8 = (1/4)^(x-5) - 8
# For f(x) = n: (1/4)^(x-5) = n+8
# x = 5 - log_4(n+8)
# Need x >= 3: log_4(n+8) <= 2, so n+8 <= 16, n <= 8
# Also n+8 > 0, so n > -8

for n in range(-7, 9):
    x_sol = 5 - log(n + 8, 4)
    x_numeric = float(N(x_sol))
    if x_numeric >= 3.0 - 1e-10:
        count_valid += 1

if count_valid == 23:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')