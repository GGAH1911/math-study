from sympy import I, expand, simplify

# 원래 식 계산
expr = (1 - 3*I) + 2*I
result = expand(expr)

# 네 답
answer = 1 - I

# 검증
if simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')