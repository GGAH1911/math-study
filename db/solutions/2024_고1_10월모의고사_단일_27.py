# 조건을 만족하는 경우 (a=3, b=18) 검증
a, b = 3, 18

# U 정의
U = set(range(1, 21))

# A: a의 배수인 U의 원소
A = {x for x in U if x % a == 0}

# B: b의 약수인 U의 원소
divisors_of_b = []
for i in range(1, b + 1):
    if b % i == 0:
        divisors_of_b.append(i)
B = {x for x in U if x in divisors_of_b}

# 조건 (가) 검증: {3, 6} ⊆ A ∩ B
intersection = A & B
condition_a = {3, 6}.issubset(intersection)

# 조건 (나) 검증: n(B - A) = 2
b_minus_a = B - A
condition_b = len(b_minus_a) == 2

# A - B의 합
a_minus_b = A - B
sum_result = sum(a_minus_b)

if condition_a and condition_b and sum_result == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')