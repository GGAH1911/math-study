from sympy import binomial, factorial

# 문제: 9C7의 값을 구하라
# 조합의 정의: nCr = n! / (r! * (n-r)!)

n = 9
r = 7

# 방법 1: sympy의 binomial 함수로 직접 계산
result_binomial = binomial(n, r)

# 방법 2: 조합의 성질을 이용한 검증
# nCr = nC(n-r) 이므로, 9C7 = 9C2
result_property = binomial(n, n - r)

# 방법 3: 조합의 정의를 직접 계산
# nCr = n! / (r! * (n-r)!)
result_formula = factorial(n) // (factorial(r) * factorial(n - r))

# 검증: 모든 방법이 같은 결과를 주는가
assert result_binomial == result_property == result_formula

# 최종 답
answer = result_binomial

# 원래 조건 확인: 답이 36인가
expected = 36
if answer == expected:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")