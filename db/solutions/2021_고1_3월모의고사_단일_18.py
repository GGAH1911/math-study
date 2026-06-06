from sympy import symbols, solve, sqrt, Rational

# 변수 정의
e, f = symbols('e f', real=True, positive=True)

# 조건 (가): EB : FD = 2 : 1
# EB = 2 - e, FD = 2 - f
# (2 - e) : (2 - f) = 2 : 1
eq1 = 2 - e - 2 * (2 - f)

# 조건 (나): 삼각형 AEF의 넓이 = 10/9
# 넓이 = (1/2) * e * f
eq2 = e * f - Rational(20, 9)

# 연립방정식 풀이
solutions = solve([eq1, eq2], [e, f])
print(f"Solutions: {solutions}")

# 주어진 답 검증
af_candidate = Rational(5, 3)
f_val = af_candidate

# e 계산
e_val = 2 * f_val - 2
print(f"e = {e_val}, f = {f_val}")

# 조건 (가) 검증: EB : FD
EB = 2 - e_val
FD = 2 - f_val
ratio = EB / FD
print(f"EB = {EB}, FD = {FD}, EB:FD = {ratio} (should be 2)")

# 조건 (나) 검증: 삼각형 넓이
area = Rational(1, 2) * e_val * f_val
print(f"Area of AEF = {area} (should be 10/9)")

if ratio == 2 and area == Rational(10, 9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')