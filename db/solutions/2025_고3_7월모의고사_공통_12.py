from sympy import symbols, solve, simplify

d = 3
a_n = lambda n: 1 + (n-1)*d

# 점화식 검증: d=3일 때 b_9 - b_3 = 27인지 확인
# b_3 = b_1 + 2
# b_9를 다시 계산
b_vals = {}
b_vals[1] = symbols('b_1')
b_vals[2] = b_vals[1] + 1
b_vals[3] = b_vals[2] + 1

for n in range(3, 9):
    if n % 3 == 0:
        b_vals[n+1] = a_n(n) + b_vals[n]
    else:
        b_vals[n+1] = b_vals[n] + 1

diff = simplify(b_vals[9] - b_vals[3])

# diff가 27이어야 함
if diff == 27:
    # 합 검증
    total = sum(a_n(k) for k in range(1, 11))
    if total == 145:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')