import sympy as sp

# 수열 계산
a = [None, sp.Rational(1, 2)]  # a[1]

# 점화식: a_{n+1} = -1/(a_n - 1)
for i in range(1, 22):
    a_n = a[-1]
    a_next = -1 / (a_n - 1)
    a.append(a_next)

# S_22 계산 (a[1]부터 a[22]까지의 합)
S_22 = sum(a[1:23])

if S_22 == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'S_22 = {S_22}')