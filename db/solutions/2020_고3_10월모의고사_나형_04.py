from sympy import symbols, limit, diff, Function, oo

# 검증용 구체적 함수: f(x) = 3x를 사용 (f'(2)=3 만족)
# 일반적으로는 어떤 함수든 f'(2)=3이면 답은 6

h = symbols('h')
x = symbols('x')

# f(x) = 3x 예시
def f(val):
    return 3*val

# 주어진 조건 확인: f'(2) = 3
# f(x) = 3x에서 f'(x) = 3이므로 f'(2) = 3 ✓

# 구하는 극한 계산
# lim_{h->0} [f(2+h)-f(2-h)]/h
numerator = f(2+h) - f(2-h)
expression = numerator / h

result = limit(expression, h, 0)

if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')