import math

def f(n):
    a = n - math.sqrt(401)
    if n % 2 == 0:
        if a > 0:
            return 2
        elif a < 0:
            return 0
        else:
            return 1
    else:
        return 1

def is_integer_log(n):
    fn = f(n)
    denom = n * (fn + 3)
    if denom <= 0:
        return False
    val = 15.0 / denom
    if val <= 0:
        return False
    log_val = math.log2(val)
    return abs(log_val - round(log_val)) < 1e-9

valid_ns = [n for n in range(2, 51) if is_integer_log(n)]
total = sum(valid_ns)

expected = {10, 15, 20, 24, 48}
if set(valid_ns) == expected and total == 117:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: valid_ns={valid_ns}, sum={total}')
