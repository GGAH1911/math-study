import math

# Verify each value of f(n)
results = {}
for n in [3, 4, 5, 6]:
    a = 2*n**2 - 9*n
    
    if n % 2 == 1:  # n is odd
        # Odd root always exists for any real number
        f_n = 1
    else:  # n is even
        if a > 0:
            f_n = 2
        elif a == 0:
            f_n = 1
        else:  # a < 0
            f_n = 0
    
    results[n] = f_n
    print(f'n={n}: 2n²-9n = {a}, f({n}) = {f_n}')

total = sum(results.values())
print(f'\nTotal: {results[3]} + {results[4]} + {results[5]} + {results[6]} = {total}')

if total == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')