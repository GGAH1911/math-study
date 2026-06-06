import sympy as sp

# a=16, b=16^(3/4)=8 으로 구체적 검증
a = sp.Integer(16)
b = sp.Rational(8, 1)  # 16^(3/4) = (2^4)^(3/4) = 2^3 = 8

# 두 점 계산
log4_a = sp.log(a, 4)   # log_4(16) = 2
log2_b = sp.log(b, 2)   # log_2(8)  = 3

# 원점과 두 점이 일직선인지: 기울기 동일 여부
slope1 = log4_a / 2     # 2/2 = 1
slope2 = log2_b / 3     # 3/3 = 1

cond_collinear = sp.simplify(slope1 - slope2) == 0

# log_a(b) 계산
result = sp.log(b, a)   # log_16(8) = 3/4
expected = sp.Rational(3, 4)

cond_answer = sp.simplify(result - expected) == 0

if cond_collinear and cond_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('collinear:', cond_collinear, 'slope1:', slope1, 'slope2:', slope2)
    print('log_a_b:', result, 'expected:', expected)
