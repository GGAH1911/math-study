from sympy import symbols, Eq, solve

# 검증: 원점을 지나고 (6, a)를 지나는 직선이 3x+2y-1=0에 수직인가
a = 4

# 원점과 (6, a)를 지나는 직선의 기울기
m_vertical = a / 6  # = 4/6 = 2/3

# 주어진 직선 3x+2y-1=0의 기울기
m_given = -3 / 2

# 수직 조건 확인: 두 기울기의 곱이 -1
product = m_vertical * m_given

if abs(product - (-1)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')