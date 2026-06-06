import sympy as sp
from sympy import symbols, diff, solve

# 변수 정의
x = symbols('x')
a_val = -2/3

# 원래 함수
def f(x_val):
    return x_val**3 - (5/2)*x_val**2 + a_val*x_val + 2

# 도함수
def f_prime(x_val):
    return 3*x_val**2 - 5*x_val + a_val

# f(2) 계산
f_2 = f(2)
print(f'f(2) = {f_2}')
print(f'|f(2)| = {abs(f_2)}')

# 접선들의 교점 확인
m_l = f_prime(0)  # 점 A에서의 기울기
m_m = f_prime(2)  # 점 B에서의 기울기

# 접선의 방정식
# l: y = m_l * x + 2
# m: y = m_m * (x - 2) + f_2

# 교점 구하기: m_l * x + 2 = m_m * (x - 2) + f_2
x_intersect = (f_2 - 2 + 2*m_m) / (m_l - m_m)
y_intersect = m_l * x_intersect + 2

print(f'교점: ({x_intersect}, {y_intersect})')
print(f'y_intersect가 0인가? {abs(y_intersect) < 1e-10}')

# 최종 답
answer = 60 * abs(f_2)
print(f'60 × |f(2)| = {answer}')

if abs(answer - 80) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')