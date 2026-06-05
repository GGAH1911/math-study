from sympy import symbols, solve, simplify
import numpy as np

m = symbols('m', real=True, integer=True)
x = symbols('x', real=True)

# 원래 함수
def f(x_val, m_val):
    return x_val**2 - 2*(m_val+1)*x_val + m_val**2 - 4

# 조건을 만족하는 정수 m 찾기
valid_count = 0
valid_m_list = []

for m_val in range(-10, 20):
    # 판별식 조건
    discriminant = 12*m_val + 25
    if discriminant <= 0:
        continue
    
    # 교점 방정식의 근 찾기
    roots = solve(x**2 - (2*m_val + 3)*x + m_val**2 - 4, x)
    if len(roots) != 2:
        continue
    
    a, b = roots[0], roots[1]
    
    # f(a) + f(b) 계산
    f_sum = f(a, m_val) + f(b, m_val)
    f_sum_simplified = simplify(f_sum)
    
    # 조건 확인: f(a) + f(b) < 16
    if f_sum_simplified < 16:
        valid_count += 1
        valid_m_list.append(m_val)

if valid_count == 9 and valid_m_list == [-2, -1, 0, 1, 2, 3, 4, 5, 6]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Count: {valid_count}, List: {valid_m_list}')