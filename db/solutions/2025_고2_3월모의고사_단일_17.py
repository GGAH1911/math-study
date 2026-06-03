def compute_g(k):
    roots = {1, 5, 1 + k, 5 + k}
    return len(roots)

solutions = []
for k in range(-100, 100):
    if compute_g(k - 7) + compute_g(k + 1) == 6:
        solutions.append(k)

answer_sum = sum(solutions)

if answer_sum == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')