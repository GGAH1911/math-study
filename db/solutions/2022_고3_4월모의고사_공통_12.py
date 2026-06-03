# 주어진 조건들을 만족하는 수열 검증
a = {1: 10, 2: 5, 3: -1, 4: -8, 5: 5, 6: 10, 7: 16, 8: 23}

# 조건 (가) 검증: 1 <= n <= 4, a_n + a_{n+4} = 15
for n in range(1, 5):
    assert a[n] + a[n+4] == 15, f'조건 (가) 위반: a_{n} + a_{n+4} = {a[n] + a[n+4]}'

# 조건 (나) 검증: n >= 5, a_{n+1} - a_n = n
for n in range(5, 8):
    assert a[n+1] - a[n] == n, f'조건 (나) 위반: a_{n+1} - a_n = {a[n+1] - a[n]}, 기댓값 = {n}'

# 합 조건 검증
assert sum(a[i] for i in range(1, 5)) == 6, f'합 조건 위반: {sum(a[i] for i in range(1, 5))}'

if a[5] == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')