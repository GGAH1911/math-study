from sympy import symbols, roots as get_roots, diff, solve

CANDIDATE = 15

x = symbols('x', real=True)

# 곡선: y = 4x^3 - 12x + 7
f = 4*x**3 - 12*x + 7

# 극값 계산
f_prime = diff(f, x)  # 12x^2 - 12
critical_pts = solve(f_prime, x)  # [-1, 1]

# 각 임계점에서의 함수값
extreme_values = [f.subs(x, pt) for pt in critical_pts]  # [15, -1]

# CANDIDATE가 극값이고 양수인지 확인
if CANDIDATE not in extreme_values or CANDIDATE <= 0:
    print("VERIFY_FAIL")
else:
    # 곡선과 직선의 교점 방정식: 4x^3 - 12x + 7 = CANDIDATE
    equation = 4*x**3 - 12*x + (7 - CANDIDATE)
    
    # 근 구하기 (multiplicity 무시)
    roots_dict = get_roots(equation, x)
    
    # 실근의 개수 (distinct roots만)
    real_roots = [r for r in roots_dict.keys() if r.is_real]
    num_real_roots = len(real_roots)
    
    # 교점이 정확히 2개인지 확인
    if num_real_roots == 2:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")