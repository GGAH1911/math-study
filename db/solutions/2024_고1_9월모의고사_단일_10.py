import sympy as sp

# 주어진 조건
x, y, a = sp.symbols('x y a', real=True)

# 구하는 직선: y절편 5/2, 기울기 3/2
line_eq = sp.Eq(y, sp.Rational(3, 2) * x + sp.Rational(5, 2))

# 점 (1, a)가 이 직선 위에 있어야 함
a_value = sp.Rational(3, 2) * 1 + sp.Rational(5, 2)

# 검증 1: a = 4
if a_value == 4:
    # 검증 2: 직선이 점 (1, 4)를 지나는가?
    y_at_1 = sp.Rational(3, 2) * 1 + sp.Rational(5, 2)
    if y_at_1 == 4:
        # 검증 3: 원래 직선과 수직인가?
        # 원래 직선: 2x + 3y + 1 = 0 → y = -2/3 x - 1/3 (기울기 -2/3)
        m1 = sp.Rational(-2, 3)
        m2 = sp.Rational(3, 2)
        if m1 * m2 == -1:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')