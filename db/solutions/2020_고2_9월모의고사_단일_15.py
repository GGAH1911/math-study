import sympy as sp

count = 0
sols = []
for m in range(-100, 101):
    a = 5 - m  # 5 + m*(-1)
    b = 5 + m  # 5 + m*1
    if a <= 0 or b <= 0:
        continue  # 정의역 밖
    f_neg1 = -sp.log(a, 3)
    f_pos1 = -sp.log(b, 3)
    if sp.simplify(f_neg1 - f_pos1) < 0:  # f(-1) < f(1)
        count += 1
        sols.append(m)

expected = 4
if count == expected and sorted(sols) == [-4, -3, -2, -1]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', count, sols)
