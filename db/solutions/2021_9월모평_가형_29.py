from itertools import combinations_with_replacement

def count_distributions():
    total = 0
    for a_A in range(2, 11):
        for a_B in range(2, 11):
            for a_C in range(2, 11):
                if a_A + a_B + a_C != 10:
                    continue
                count = 0
                for w_A in range(min(4, a_A) + 1):
                    for w_B in range(min(4 - w_A, a_B) + 1):
                        w_C = 4 - w_A - w_B
                        if 0 <= w_C <= a_C:
                            count += 1
                total += count
    return total

result = count_distributions()
if result == 168:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 168, got {result}')