import math

def a_n(n):
    return math.log2(math.sqrt(2*(n+1)/(n+2)))

def sum_a(m):
    return sum(a_n(k) for k in range(1, m+1))

# Check candidates
candidates = [6, 30, 126]
results = []

for m in candidates:
    s = sum_a(m)
    is_int = abs(s - round(s)) < 1e-9
    int_val = round(s) if is_int else None
    results.append((m, s, is_int, int_val, int_val <= 100 if int_val else False))
    print(f'm={m}: sum={s:.10f}, int={int_val}, valid={int_val is not None and int_val <= 100 and int_val > 0}')

valid_m = [m for m, s, is_int, int_val, valid in results if valid]
total = sum(valid_m)
print(f'Valid m values: {valid_m}')
print(f'Sum: {total}')
print('VERIFY_PASS' if total == 162 else 'VERIFY_FAIL')