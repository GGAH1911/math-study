from sympy import symbols, limit, Rational

CANDIDATE = 40

x = symbols('x', real=True)

# 문제의 주어진 조건들로부터 유도된 함수
# f(x) = (1/12)*x^2 - (1/3)*x
a = Rational(1, 12)
b = Rational(-1, 3)

def f(t):
    """이차함수: f(t) = a*t^2 + b*t, f(0)=0"""
    return a * t**2 + b * t

# ===== 조건 (가) 검증 =====
# lim_{x->0-} [|x| - f(x)] / [x + f(x)] * lim_{x->0+} [|x| - f(x)] / [x + f(x)] = -2
# x < 0에서 |x| = -x, x > 0에서 |x| = x

left_limit = limit((-x - f(x)) / (x + f(x)), x, 0, '-')
right_limit = limit((x - f(x)) / (x + f(x)), x, 0, '+')
product = left_limit * right_limit

cond_a = (product == -2)

# ===== 조건 (나) 검증 =====
# lim_{x->a} f(x-4)*f(x+1) / (|x| - 3) 의 값이 존재하지 않는 a의 개수 = 1
# 분모가 0인 점: x = ±3
# x = 3에서: f(4) = 0이므로 극한 존재 가능
# x = -3에서: f(-7)*f(-2) ≠ 0이므로 극한 불존재

f_4 = f(4)
f_neg7_times_f_neg2 = f(-7) * f(-2)

cond_b = (f_4 == 0 and f_neg7_times_f_neg2 != 0)

# ===== 최고차항 계수 양수 확인 =====
cond_leading_positive = (a > 0)

# ===== 최종 답 계산 및 검증 =====
f_24 = f(24)

if cond_a and cond_b and cond_leading_positive and f_24 == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")