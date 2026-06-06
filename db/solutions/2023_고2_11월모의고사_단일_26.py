from sympy import symbols, solve, diff

CANDIDATE = '12'

t = symbols('t', real=True)

# 점 P의 속도: v1(t) = x1'(t) = 3t^2 - 6t - 24
v1 = 3*t**2 - 6*t - 24
v1_prime = diff(v1, t)  # v1_prime = 6t - 6

# v1(t) = 0의 해 구하기
v1_roots = solve(v1, t)

# t > 0인 근 중에서 부호 변화가 있는 근 찾기
k = None
for root in v1_roots:
    if root > 0:
        # v1'(root) != 0이면 t=root에서 부호 변화 있음
        if v1_prime.subs(t, root) != 0:
            k = float(root)
            break

if k is not None:
    # 점 Q의 속도: v2(t) = x2'(t) = 2t - a
    # 두 점이 동시에 운동 방향이 바뀌므로: v2(k) = 0
    # 2k - a = 0
    a = 2 * k
    
    # a + k 계산
    answer = a + k
    
    # CANDIDATE와 비교
    try:
        candidate_int = int(CANDIDATE)
        if answer == candidate_int:
            print("VERIFY_PASS")
        else:
            print("VERIFY_FAIL")
    except:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")