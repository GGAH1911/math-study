from sympy import symbols, solve, simplify, Rational

x, y, a = symbols('x y a', real=True)

# a = 7/2로 설정
a_val = Rational(7, 2)

# 함수: f(x) = 4/(2x-7) + a
def f(x_val, a_val):
    return 4/(2*x_val - 7) + a_val

# 정의역: x ≠ 7/2
# 정의역은 R \ {7/2}

# 치역 확인: y = 4/(2x-7) + a에서 y ≠ a인지 확인
# y - a = 4/(2x-7)
# 2x - 7 = 4/(y-a) (y ≠ a일 때)
# x = 7/2 + 2/(y-a)

# y = a일 때: x를 구할 수 없음 (2/(y-a)가 정의 불가)
# 따라서 치역은 R \ {a}

# 정의역 = R \ {7/2}
# 치역 = R \ {a}
# 정의역 = 치역이면 a = 7/2

if a_val == Rational(7, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')