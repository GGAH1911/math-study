f = {1: 4, 2: 3, 3: 2}
g = {2: 1, 3: 5, 4: 2}
result = g[f[2]]
print('VERIFY_PASS' if result == 5 else 'VERIFY_FAIL')