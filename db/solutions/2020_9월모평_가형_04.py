from itertools import product

# 6의 약수
divisors_of_6 = [1, 2, 3, 6]

# 2의 배수인 한 자리 숫자
even_digits = [0, 2, 4, 6, 8]

# 조건을 만족하는 두 자리 수 찾기
count = 0
valid_numbers = []
for tens in divisors_of_6:
    for ones in even_digits:
        number = tens * 10 + ones
        if 10 <= number <= 99:  # 두 자리
            if number % 2 == 0:  # 2의 배수
                count += 1
                valid_numbers.append(number)

if count == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')