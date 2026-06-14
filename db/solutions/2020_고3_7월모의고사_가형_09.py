from itertools import product

# 두 주사위 모든 경우
all_outcomes = list(product(range(1, 7), repeat=2))

# 곱이 짝수인 경우
product_even = [out for out in all_outcomes if (out[0] * out[1]) % 2 == 0]

# 곱이 짝수이면서 합이 짝수인 경우
product_even_sum_even = [out for out in product_even if (out[0] + out[1]) % 2 == 0]

# 확률 계산
if len(product_even) > 0:
    prob = len(product_even_sum_even) / len(product_even)
    expected = 1/3
    if abs(prob - expected) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')