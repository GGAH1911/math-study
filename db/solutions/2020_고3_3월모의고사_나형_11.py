from sympy import symbols, solve, simplify

# 변수 정의
d, r = symbols('d r', real=True)

# 조건식
eq1 = 3*r**2 + 3 + d  # b_3 = -a_2 형태로 정리
eq2 = (3 + d) + 3*r - (3 + 2*d) - 3*r**2  # a_2 + b_2 = a_3 + b_3

# 연립방정식 풀이
sol = solve([eq1, eq2], [d, r])

# a_3 계산
for d_val, r_val in sol:
    a3 = 3 + 2*d_val
    
    # 검증: 조건 확인
    a2 = 3 + d_val
    b2 = 3*r_val
    b3 = 3*r_val**2
    
    cond1 = simplify(b3 + a2)
    cond2 = simplify(a2 + b2 - (3 + 2*d_val) - b3)
    
    if cond1 == 0 and cond2 == 0:
        if a3 == -9:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')