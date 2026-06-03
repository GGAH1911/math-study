import sympy as sp
n_var = sp.Symbol('n', integer=True, positive=True)
expr = n_var**2 - 16*n_var + 48
results = []
for n in range(2, 11):
    value = expr.subs(n_var, n)
    if value > 0:
        if n % 2 == 0:
            count = 2  # positive n-th roots: +a and -a
        else:
            count = 1  # positive n-th root only
    elif value == 0:
        count = 1
    else:  # value < 0
        if n % 2 == 1:
            count = 1  # negative n-th root exists
        else:
            count = 0  # no real n-th roots
    results.append(count)
total = sum(results)
if total == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')