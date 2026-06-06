# 등차수열 검증: a_n = a_1 + (n-1)d
a_1 = 15
d = -2

# 일반항 계산
def a_n(n):
    return a_1 + (n - 1) * d

# 주어진 조건 확인
condition1 = (a_n(6) == 5)
condition2 = (a_n(5) == a_n(2) - 6)

print(f'a_6 = {a_n(6)}, 조건1(a_6=5): {condition1}')
print(f'a_5 = {a_n(5)}, a_2 = {a_n(2)}, a_5=a_2-6: {condition2}')

if condition1 and condition2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')