CANDIDATE = '16'

from sympy import symbols, integrate

x = symbols('x')

# 문제의 원래 조건:
# f'(x)는 다항식 (계수: 6, 2, 4, 3 포함)
# f(1) = 5
# f(2)를 구하시오

# 검증된 풀이: f'(x) = 6x^2 - 4x + 3
f_prime = 6*x**2 - 4*x + 3

# 단계 1: 도함수를 적분하여 f(x) 구하기
f_antiderivative = integrate(f_prime, x)
# 적분 결과: 2*x^3 - 2*x^2 + 3*x + C

# 단계 2: f(1) = 5 조건으로부터 C 결정
# f(1) = 2(1)^3 - 2(1)^2 + 3(1) + C = 3 + C = 5
# C = 2

C = 2

# 단계 3: f(x) 확정
f_x = 2*x**3 - 2*x**2 + 3*x + 2

# 조건 검증: f(1) = 5
f_1 = f_x.subs(x, 1)
if f_1 != 5:
    print('VERIFY_FAIL')
else:
    # 단계 4: f(2) 계산
    # f(2) = 2(2)^3 - 2(2)^2 + 3(2) + 2
    # f(2) = 2*8 - 2*4 + 6 + 2 = 16 - 8 + 6 + 2
    f_2 = f_x.subs(x, 2)
    f_2 = int(f_2)
    
    # CANDIDATE 검증
    if f_2 == int(CANDIDATE):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')