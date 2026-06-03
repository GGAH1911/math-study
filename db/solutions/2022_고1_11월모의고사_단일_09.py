f = {3: 1, 6: 4, 9: 7}
g = {1: 3, 4: 6, 7: 9}
g_of_f = {x: g[f[x]] for x in f}
g_of_f_inv = {v: k for k, v in g_of_f.items()}
result = g_of_f[3] + g_of_f_inv[9]
assert result == 12, f'Expected 12, got {result}'
print('VERIFY_PASS')