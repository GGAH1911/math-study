from sympy import sqrt, I, expand, simplify

# 원래 문제의 식
result = expand((sqrt(2) + sqrt(-2))**2)
print(f'계산 결과: {result}')

# 답 검증
answer = 4*I
if simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')