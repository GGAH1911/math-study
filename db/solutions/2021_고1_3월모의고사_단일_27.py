from sympy import sqrt, simplify, Rational, Abs

CANDIDATE = 48

# 원래 문제의 조건 인코딩:
# 1. 이차함수: y = ax^2 (a > 0)
# 2. 포물선 위의 두 점 A(p, 3), B(q, 3)
#    - ap^2 = 3, aq^2 = 3 조건을 만족
# 3. 점 C(-1, -1), D(1, -1)
# 4. 사각형 ACDB의 넓이가 자연수

a = CANDIDATE

# 조건 1: 포물선 y = ax^2 위의 점 A, B
# ap^2 = 3에서 p^2 = 3/a
# p < 0, q > 0 (y축 대칭, p < q)
p = -sqrt(Rational(3, a))
q = sqrt(Rational(3, a))

# 포물선 위의 점인지 검증
verify_A = simplify(a * p**2 - 3)
verify_B = simplify(a * q**2 - 3)

if verify_A != 0 or verify_B != 0:
    print("VERIFY_FAIL")
    exit()

# 조건 2: 사각형 ACDB의 넓이 계산
# 신발끈 공식(Shoelace formula)으로 사각형 넓이 계산
A = (p, 3)
C = (-1, -1)
D = (1, -1)
B = (q, 3)

vertices = [A, C, D, B]
shoelace_sum = 0

for i in range(4):
    j = (i + 1) % 4
    shoelace_sum += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]

area = Abs(shoelace_sum) / 2
area = simplify(area)

# 조건 3: 넓이가 자연수인지 검증
# a = 48일 때:
# area = 4*sqrt(3/48) + 4 = 4*sqrt(1/16) + 4 = 4*(1/4) + 4 = 1 + 4 = 5

area_numeric = float(area)

# 자연수 판정: 양수이면서 정수값
if area_numeric > 0 and area_numeric == int(area_numeric):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")