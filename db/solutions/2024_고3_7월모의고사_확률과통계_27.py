from math import factorial

def count_arrangements(total, p_cond):
    count = 0
    valid_triples = []
    for p in range(1, total):
        for q in range(p+1, total):
            r = total - p - q
            if r > q:
                valid_triples.append((p, q, r))
                ways = factorial(total) // (factorial(p) * factorial(q) * factorial(r))
                count += ways
    return count, valid_triples

total = 8
result, triples = count_arrangements(total, None)
print(f'Valid triples: {triples}')
print(f'Total arrangements: {result}')

if result == 448:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
