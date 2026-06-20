from sympy import symbols, solve, diff, factor

CANDIDATE = 12

x = symbols('x')
k = CANDIDATE

# 원래 방정식
f = x**3 - x**2 - 8*x + k

# 실근 구하기
roots = solve(f, x)
real_roots = [r for r in roots if r.is_real]

# 서로 다른 실근의 개수
num_distinct = len(set(real_roots))

if num_distinct == 2:
    # 중근이 있는지 확인
    f_prime = diff(f, x)
    critical_points = solve(f_prime, x)
    has_critical_root = any(f.subs(x, cp) == 0 for cp in critical_points)
    
    if has_critical_root and k > 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')