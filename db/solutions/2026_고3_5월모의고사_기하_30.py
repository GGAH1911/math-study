from sympy import symbols, sqrt, solve, simplify, Eq

CANDIDATE = 80

# 문제 조건으로부터 도출된 핵심 식:
# (1) 타원의 접선 조건: Q_x = 1/c 이고 Q는 타원 위 → b² = 1 - 1/c²
# (2) 거리 조건 |PQ| = |PF'| + b²를 정리 → b²(√(c²+1) + 1) = 2
# 쌍곡선 정의: c² = 1 + a²

c_sq = symbols('c_sq', positive=True, real=True)

# 식 (1)과 (2)를 연립하여 c²를 구한다
eq = Eq((1 - 1/c_sq) * (sqrt(c_sq + 1) + 1), 2)
c_sq_solutions = solve(eq, c_sq)

# c² > 1인 유효한 해 찾기 (a² = c² - 1 > 0이어야 함)
c_sq_val = None
for sol in c_sq_solutions:
    try:
        val = float(sol.evalf())
        if val > 1:
            c_sq_val = sol
            break
    except:
        pass

if c_sq_val is not None:
    # a² = c² - 1 (쌍곡선의 초점 공식)
    a_sq = c_sq_val - 1
    
    # b² = 1 - 1/c² (접선 조건)
    b_sq = 1 - 1/c_sq_val
    
    # 최종 답: 30(a² + b²)
    answer = 30 * (a_sq + b_sq)
    answer = simplify(answer)
    
    # CANDIDATE와 비교
    if simplify(answer - CANDIDATE) == 0:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")