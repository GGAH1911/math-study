from sympy import *

# 매개변수 e
e = symbols('e', real=True, positive=True)

# F의 좌표
F_x = 2*e**2 / (e**2 + 1)
F_y = 2*e / (e**2 + 1)

# 사각형 ABFE의 넓이 (신발끈 공식)
# A(0,0), B(1,0), F, E(0,e)
area = e  # 계산 결과

# 조건 (나): 넓이 = 1/3
e_solution = solve(area - Rational(1,3), e)
print(f'e = {e_solution}')

e_val = Rational(1, 3)

# F의 구체적 좌표
F_x_val = 2*e_val**2 / (e_val**2 + 1)
F_y_val = 2*e_val / (e_val**2 + 1)

print(f'F = ({F_x_val}, {F_y_val})')

# 검증: AB = FB = 1
AB = 1
FB = sqrt((F_x_val - 1)**2 + F_y_val**2)
print(f'AB = {AB}, FB = {simplify(FB)}')
assert simplify(FB - 1) == 0

# 검증: AE = FE = 1/3
AE = e_val
FE = sqrt(F_x_val**2 + (F_y_val - e_val)**2)
print(f'AE = {AE}, FE = {simplify(FE)}')
assert simplify(FE - e_val) == 0

# tan(∠ABF) 계산
# B(1,0), F(1/5, 3/5)
# F에서 x축에 내린 수선의 발: (1/5, 0)
height = F_y_val
base = 1 - F_x_val
tan_ABF = height / base

print(f'height = {height}, base = {base}')
print(f'tan(∠ABF) = {tan_ABF}')

if tan_ABF == Rational(3, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')