from sympy import symbols, solve, summation

# 공비 r = 2, 첫째항 a = 1/2
r = 2
a = 1/2

def S(n):
    return a * (r**n - 1) / (r - 1)

# 주어진 조건 검증
result = sum((-1)**k * S(k) for k in range(1, 7))
print(f'Condition check: {result}')

# 답 계산
S2 = S(2)
S7 = S(7)
answer = S2 + S7

if result == 21 and answer == 65:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')