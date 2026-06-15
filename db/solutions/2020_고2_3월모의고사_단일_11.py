import sympy as sp

# 점 P(a, b)가 원 x^2 + y^2 = 1 위에 있음
a, b = sp.symbols('a b', real=True, positive=True)

# 조건 1: P가 원 위의 점
eq1 = a**2 + b**2 - 1

# 조건 2: P에서의 접선이 (0,3)을 지남
# 접선 방정식: ax + by = 1
# 점 (0,3) 대입: a*0 + b*3 = 1
eq2 = 3*b - 1

# eq2에서 b 구하기
b_val = sp.solve(eq2, b)[0]
print(f'b = {b_val}')

# b를 eq1에 대입하여 a 구하기
a_val = sp.solve(eq1.subs(b, b_val), a)
print(f'a = {a_val}')

# 양수 해
a_answer = [x for x in a_val if x > 0][0]
print(f'P의 x좌표 = {a_answer}')

# 검증
point_a = a_answer
point_b = b_val
print(f'\n검증:')
print(f'a^2 + b^2 = {point_a**2 + point_b**2}')
print(f'접선이 (0,3)을 지나는가: {point_a*0 + point_b*3}')

if point_a**2 + point_b**2 == 1 and point_a*0 + point_b*3 == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')