import sympy as sp
from sympy import sqrt, symbols, solve

k_sq = 5
k = sqrt(k_sq)

a = k * (sqrt(2) - 1)
b = -k * (sqrt(2) + 1)

# 점 A가 곡선 위에 있는지 확인
x_a, y_a = a, a + k
result_a = x_a**2 - 2*x_a*y_a + 2*y_a**2
result_a_simplified = sp.simplify(result_a)

# 점 B가 곡선 위에 있는지 확인
x_b, y_b = b, b + k
result_b = x_b**2 - 2*x_b*y_b + 2*y_b**2
result_b_simplified = sp.simplify(result_b)

# 접선 기울기
m_a = k / (a + 2*k)
m_b = k / (b + 2*k)
m_product = sp.simplify(m_a * m_b)

# 수직성 확인
if result_a_simplified == 15 and result_b_simplified == 15 and m_product == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')