from sympy import symbols, solve, Rational

CANDIDATE = 9

# 단계 1: 사각형 ABCD의 넓이 조건으로부터 a 결정
# A(-3, -a), B(1, 0), C(3, 3a), D(-3, 0)
# 신발끈 공식: Area = 1/2 * |x1(y2-y4) + x2(y3-y1) + x3(y4-y2) + x4(y1-y3)|
#                  = 1/2 * |(-3)(0-0) + 1(3a-(-a)) + 3(0-0) + (-3)((-a)-3a)|
#                  = 1/2 * |0 + 4a + 0 + 12a|
#                  = 1/2 * 16a = 8a

a_sym = symbols('a', positive=True)
area_eq_solutions = solve(8*a_sym - 16, a_sym)
a_value = area_eq_solutions[0]
assert a_value == 2, f'a must equal 2, got {a_value}'
a = 2

# 단계 2: f(x)의 꼭짓점이 A(-3, -a)이고 B(1, 0)을 지남
# f(x) = k(x+3)^2 - a 형태
# f(1) = 0 조건: k(1+3)^2 - a = 0 => 16k = a => k = a/16 = 2/16 = 1/8

k_coeff = Rational(1, 8)

def f(x):
    return k_coeff * (x + 3)**2 - a

# f(1) = 0 검증
assert f(1) == 0, f'f(1) must be 0, got {f(1)}'

# 단계 3: g(x)의 꼭짓점이 C(3, 3a)이고 y절편이 선분 CD 위에 있음
# g(x) = m(x-3)^2 + 3a 형태
# 선분 CD: C(3, 6), D(-3, 0)
# 기울기 = (6-0)/(3-(-3)) = 1, 직선: y = x + 3
# g(0) = 3 조건: m(0-3)^2 + 3a = 3 => 9m + 6 = 3 => m = -1/3

m_coeff = Rational(-1, 3)

def g(x):
    return m_coeff * (x - 3)**2 + 3*a

# g(0) = 3 검증 (y절편이 선분 CD 위에 있음)
assert g(0) == 3, f'g(0) must be 3, got {g(0)}'

# 단계 4: f(-1) 계산
f_at_neg1 = f(-1)  # (1/8)(2)^2 - 2 = 1/2 - 2 = -3/2
assert f_at_neg1 == Rational(-3, 2), f'f(-1) must be -3/2, got {f_at_neg1}'

# 단계 5: g(-3) 계산
g_at_neg3 = g(-3)  # (-1/3)(-6)^2 + 6 = (-1/3)(36) + 6 = -12 + 6 = -6
assert g_at_neg3 == -6, f'g(-3) must be -6, got {g_at_neg3}'

# 단계 6: f(-1) × g(-3) 계산
product = f_at_neg1 * g_at_neg3  # (-3/2) × (-6) = 9

# 단계 7: CANDIDATE와 비교
if product == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')