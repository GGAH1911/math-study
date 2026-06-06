from math import comb
w, b = 27, 13
assert w + b == 40
p = comb(w, 2) / comb(40, 2)
q = (w * b) / comb(40, 2)
r = comb(b, 2) / comb(40, 2)
assert abs(p - q) < 1e-10, f'p={p}, q={q}'
result = 60 * r
assert abs(result - 6) < 1e-10, f'60r={result}'
print('VERIFY_PASS')