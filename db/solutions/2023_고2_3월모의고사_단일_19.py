from sympy import symbols, solve, Integer, simplify, sqrt, Rational

x = symbols('x', real=True)
forced = [Integer(0), Integer(-2), Integer(2)]

# 새 원소 x 후보: x^2-2 가 A의 어떤 원소가 되는 경우
candidates = []
for target in [Integer(0), Integer(-2), Integer(2)]:
    for s in solve(x**2 - 2 - target, x):
        if s not in forced and s not in candidates:
            candidates.append(s)
for s in solve(x**2 - 2 - x, x):
    if s not in forced and s not in candidates:
        candidates.append(s)

valid = []
for c in candidates:
    A = forced + [c]
    if len({simplify(a) for a in A}) != 4:
        continue
    ok = True
    for a in A:
        img = simplify(a**2 - 2)
        found = any(simplify(img - b) == 0 for b in A)
        if not found:
            ok = False
            break
    if ok:
        valid.append(A)

count = len(valid)
print('VERIFY_PASS' if count == 3 else 'VERIFY_FAIL')
