from sympy import symbols, Rational, simplify

x = symbols('x')

AD = x**2 - 2*x + 3
BC = 2*x**2 + x + 6
height = 4

# 사다리꼴 ABCD 넓이
area_ABCD = Rational(1, 2) * (AD + BC) * height
area_ABCD = simplify(area_ABCD)  # 6x^2 - 2x + 18

# E는 CD의 중점 → E의 높이(BC 기준) = 4/2 = 2
# 삼각형 BEC: 밑변 BC, 높이 2
area_BEC = Rational(1, 2) * BC * 2
area_BEC = simplify(area_BEC)  # 2x^2 + x + 6

# 사각형 ABED 넓이
area_ABED = simplify(area_ABCD - area_BEC)

expected = 4*x**2 - 3*x + 12

if simplify(area_ABED - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Got: {area_ABED}, Expected: {expected}')
