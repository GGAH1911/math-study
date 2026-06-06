from sympy import symbols, summation

# 검증: 조건을 만족하는 수열로 답 확인
# 간단한 경우: 홀수 항들의 평균 = 12/10, 짝수 항들의 평균 = 20/10
a = {}
for k in range(1, 11):
    a[2*k-1] = 1.2  # 홀수 인덱스 항
    a[2*k] = 2.0    # 짝수 인덱스 항

# 조건 검증
sum_odd = sum(a[2*k-1] for k in range(1, 11))
sum_even = sum(a[2*k] for k in range(1, 11))
assert abs(sum_odd - 12) < 1e-10, f'Odd sum check failed: {sum_odd}'
assert abs(sum_even - 20) < 1e-10, f'Even sum check failed: {sum_even}'

# 답 계산
result = sum((-1)**k * a[k] for k in range(1, 21))

if abs(result - 8) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')