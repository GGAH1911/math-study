from sympy import *
a = symbols('a', real=True, positive=True)
k = symbols('k', real=True, positive=True)

# 두 곡선이 만나고 접선이 수직
eq1 = Eq(k*exp(a) + 1, a**2 - 3*a + 4)
eq2 = Eq(k*exp(a) * (2*a - 3), -1)

# eq1에서 k*e^a 표현
ke_a = a**2 - 3*a + 3

# eq2에 대입
cubic_eq = Eq((a**2 - 3*a + 3)*(2*a - 3), -1)
cubic_expanded = expand(cubic_eq.lhs - cubic_eq.rhs)
print(f'Cubic equation: {cubic_expanded} = 0')

# a의 해
a_solutions = solve(cubic_expanded, a)
print(f'Solutions for a: {a_solutions}')

# 실수 해만 선택
real_a = [sol for sol in a_solutions if sol.is_real]
print(f'Real solutions: {real_a}')

# a=1일 때 k 계산
for a_val in real_a:
    k_val = (a_val**2 - 3*a_val + 3) / exp(a_val)
    k_simplified = simplify(k_val)
    print(f'a = {a_val}: k = {k_simplified}')
    
    # 검증: 두 조건 확인
    curve1_y = k_val * exp(a_val) + 1
    curve2_y = a_val**2 - 3*a_val + 4
    m1 = k_val * exp(a_val)
    m2 = 2*a_val - 3
    
    print(f'  Curve 1 y-value: {simplify(curve1_y)}')
    print(f'  Curve 2 y-value: {simplify(curve2_y)}')
    print(f'  m1 = {simplify(m1)}, m2 = {simplify(m2)}')
    print(f'  m1 * m2 = {simplify(m1 * m2)}')
    
    if abs(simplify(m1 * m2) + 1) < 1e-10:
        print(f'VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL')