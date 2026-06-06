from sympy import symbols, solve

# 검증: a_n + a_{n+4} = 12를 만족하면서 합이 96인지 확인
# 간단한 예: a_1=a, a_2=b, a_3=c, a_4=d로 놓으면
# a_5 = 12-a, a_6 = 12-b, a_7 = 12-c, a_8 = 12-d
# 합: a + b + c + d + (12-a) + (12-b) + (12-c) + (12-d) = 48
# 주기 8이므로 16개 합 = 96

# 구체적 예로 검증
a = [0] * 17  # index 0 unused, 1-16 사용
a[1], a[2], a[3], a[4] = 1, 2, 3, 4  # 임의로 설정

# a_n + a_{n+4} = 12로부터 a_5~a_8 결정
for n in range(1, 5):
    a[n+4] = 12 - a[n]

# a_9~a_16 (주기성에 의해 a_1~a_8과 동일)
for n in range(1, 9):
    a[n+8] = a[n]

# 모든 조건 검증
valid = True
for n in range(1, 13):
    if a[n] + a[n+4] != 12:
        valid = False
        print(f'VERIFY_FAIL: a[{n}] + a[{n+4}] = {a[n]} + {a[n+4]} = {a[n] + a[n+4]} ≠ 12')

if valid:
    total = sum(a[1:17])
    if total == 96:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: sum = {total} ≠ 96')
else:
    print('VERIFY_FAIL')