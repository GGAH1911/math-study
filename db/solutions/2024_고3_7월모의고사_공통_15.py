def next_term(a):
    if a % 2 == 0 and a // 2 >= 1:
        return a // 2
    else:
        return (a - 1) ** 2

def compute_a7(a1):
    a = a1
    for _ in range(6):
        a = next_term(a)
    return a

valid_a1 = [a1 for a1 in range(1, 10000) if compute_a7(a1) == 1]
total = sum(valid_a1)
if total == 125:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: found {valid_a1}, sum={total}')