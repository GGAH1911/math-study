from sympy import symbols, solve, simplify

# 등차수열 정의: a_n = 2(7-n)
def a(n):
    return 2 * (7 - n)

# S_n과 T_n 계산 (n=15)
S_15 = sum(a(k) for k in range(1, 16))
T_15 = sum(abs(a(k)) for k in range(1, 16))

# 조건 검증
print(f'a_6={a(6)}, a_7={a(7)}, a_8={a(8)}')
print(f'a_7 == a_6 + a_8: {a(7) == a(6) + a(8)}')

# 조건 (나) 검증 (n=6,7,8)
for n in [6, 7, 8]:
    S_n = sum(a(k) for k in range(1, n+1))
    T_n = sum(abs(a(k)) for k in range(1, n+1))
    print(f'S_{n} + T_{n} = {S_n + T_n}')

print(f'\nT_15 = {T_15}')
if T_15 == 114:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')