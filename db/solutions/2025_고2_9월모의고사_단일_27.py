import math

# f(x) = 3*sin(π/4 * x) + 1
# Check all natural numbers n where f(x) = n has solutions in [0,8]

total_sum = 0
for n in [1, 2, 3, 4]:
    # Solve 3*sin(π/4 * x) + 1 = n
    # sin(π/4 * x) = (n-1)/3
    sin_val = (n - 1) / 3
    
    if abs(sin_val) > 1:
        continue
    
    solutions = []
    
    if sin_val == 0:
        # x = 0, 4, 8
        solutions = [0, 4, 8]
    elif sin_val == 1:
        # π/4 * x = π/2 → x = 2
        solutions = [2]
    else:
        # Two solutions in [0, 2π]
        theta1 = math.asin(sin_val)
        theta2 = math.pi - theta1
        x1 = 4 * theta1 / math.pi
        x2 = 4 * theta2 / math.pi
        if 0 <= x1 <= 8:
            solutions.append(x1)
        if 0 <= x2 <= 8:
            solutions.append(x2)
    
    # Verify solutions
    for x in solutions:
        f_x = 3 * math.sin(math.pi / 4 * x) + 1
        if not (abs(f_x - n) < 1e-9 and f_x > 0 and abs(f_x - round(f_x)) < 1e-9):
            print('VERIFY_FAIL')
            exit()
    
    total_sum += sum(solutions)

if abs(total_sum - 22) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')