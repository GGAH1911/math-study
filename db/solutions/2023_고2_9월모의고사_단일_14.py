def count_real_nth_roots(a, n):
    if n % 2 == 1:
        return 1
    else:
        if a > 0:
            return 2
        elif a == 0:
            return 1
        else:
            return 0

def f(n):
    a = n**2 - 15*n + 50
    return count_real_nth_roots(a, n)

results = {n: f(n) for n in range(4, 13)}

satisfying = [n for n in range(4, 12) if results[n] == results[n+1]]
total = sum(satisfying)

if total == 19 and set(satisfying) == {9, 10}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'satisfying={satisfying}, sum={total}')