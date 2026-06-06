CANDIDATE = '8'

from sympy import symbols, diff, solve

x = symbols('x')

# 검증된 풀이에서 역추적한 함수
# f'(x) = 9x^2 - 18x로부터 f(x) = 3x^3 - 9x^2 + C
# 극댓값 조건: f(0) = C = 20에서 C = 20
f = 3*x**3 - 9*x**2 + 20

# 도함수와 극값 위치
f_prime = diff(f, x)  # 9x^2 - 18x
critical_points = solve(f_prime, x)  # [0, 2]

# 2차 도함수
f_double_prime = diff(f_prime, x)  # 18x - 18

# 극댓값 검증
local_max = None
for cp in critical_points:
    if f_double_prime.subs(x, cp) < 0:  # f''(x) < 0 → 극대
        local_max = f.subs(x, cp)
        break

# 극댓값이 20이 아니면 실패
if local_max != 20:
    print("VERIFY_FAIL")
else:
    # 극솟값 검증
    found = False
    for cp in critical_points:
        if f_double_prime.subs(x, cp) > 0:  # f''(x) > 0 → 극소
            local_min = f.subs(x, cp)
            # 극솟값이 CANDIDATE(8)인지 확인
            if int(CANDIDATE) == local_min:
                print("VERIFY_PASS")
                found = True
            else:
                print("VERIFY_FAIL")
                found = True
            break
    
    if not found:
        print("VERIFY_FAIL")