from sympy import factorint

def get_distinct_prime_count(n):
    factors = factorint(n)
    return len(factors)

n = 84

# 조건 (가) 확인: 4의 배수
condition_a = (n % 4 == 0)

# 조건 (나) 확인: 소인수 개수가 3
condition_b = (get_distinct_prime_count(n) == 3)

if condition_a and condition_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')