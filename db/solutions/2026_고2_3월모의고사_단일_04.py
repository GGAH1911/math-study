f = {1: 3, 2: 1, 3: 5, 4: 2, 5: 4}
assert set(f.values()) == {1,2,3,4,5}, 'not bijection'
f_inv = {v: k for k, v in f.items()}
result = f_inv[5]
print('VERIFY_PASS' if result == 3 else 'VERIFY_FAIL')