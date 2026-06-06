from sympy import Rational

CANDIDATE = 224

# 풀이로부터 도출된 파라미터
a = Rational(18, 5)  # a = 18/5
p = Rational(25, 4)  # 이차함수 이차항 계수

# 이차함수 정의: f(x) = p(x-4)^2 - 1
def f(x):
    return p * (x - 4)**2 - 1

# g(x) 정의 (문제 조건):
# 0 <= x < a: g(x) = sin(3x) (또는 sin(3π*x/a))
# x >= a: g(x) = f(x)

# 검산: g(10) 계산
# 10 >= 18/5 = 3.6 이므로 g(10) = f(10)
result = f(10)

# 계산 과정 검증:
# result = (25/4) * (10-4)^2 - 1
#        = (25/4) * 36 - 1
#        = 900/4 - 1
#        = 225 - 1
#        = 224

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")