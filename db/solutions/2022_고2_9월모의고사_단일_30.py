from sympy import symbols, solve, Rational, N

CANDIDATE = 53

k = 4

def verify():
    """
    원래 문제 조건으로 CANDIDATE 검증:
    - 곡선: y = 2*sin(n*pi*x + pi/2) + |k*sin^2(n*pi*x) - (k-1)|
           = 2*cos(n*pi*x) + |k*sin^2(n*pi*x) - k + 1|
           u = cos(n*pi*x)로 치환 → y = 2u + |1 - k*u^2| = g(u)
    - 짝수 n: 직선 y = -k/(2n)과의 교점 개수
    - 홀수 n: 직선 y = (k+1)/n과의 교점 개수
    """
    u = symbols('u', real=True)
    sum_a = 0
    
    for n in range(1, 6):
        # 직선의 y값
        if n % 2 == 0:  # 짝수
            L = Rational(-k, 2*n)
        else:  # 홀수
            L = Rational(k + 1, n)
        
        # g(u) = 2u + |1 - k*u^2|를 L과 같게 놓기
        # Case 1: 1 - k*u^2 >= 0 일 때
        # g = 2u + (1 - k*u^2)
        eq1 = 2*u + 1 - k*u**2 - L
        sols1 = solve(eq1, u)
        
        # Case 2: 1 - k*u^2 < 0 일 때
        # g = 2u - (1 - k*u^2) = 2u - 1 + k*u^2
        eq2 = 2*u - 1 + k*u**2 - L
        sols2 = solve(eq2, u)
        
        valid_u = []
        
        # Case 1 해 검증 (-1 <= u <= 1, 1 - k*u^2 >= 0)
        for sol in sols1:
            val = float(N(sol))
            if -1 <= val <= 1:
                # Case 1 조건: 1 - k*u^2 >= 0
                if 1 - k*val*val >= -1e-9:
                    # 중복 제거
                    if not any(abs(val - v) < 1e-9 for v in valid_u):
                        valid_u.append(val)
        
        # Case 2 해 검증 (-1 <= u <= 1, 1 - k*u^2 < 0)
        for sol in sols2:
            val = float(N(sol))
            if -1 <= val <= 1:
                # Case 2 조건: 1 - k*u^2 < 0
                if 1 - k*val*val < 1e-9:
                    # 중복 제거
                    if not any(abs(val - v) < 1e-9 for v in valid_u):
                        valid_u.append(val)
        
        # 각 u에 대해 cos(n*pi*x) = u의 [0, 2] 범위에서의 해의 개수
        # x ∈ [0, 2] → n*pi*x ∈ [0, 2n*pi]
        # cos(θ) = u (θ ∈ [0, 2n*pi])의 해의 개수:
        #   |u| < 1: 2n개
        #   u = 1: n+1개
        #   u = -1: n개
        a_n = 0
        for u_val in valid_u:
            if abs(u_val - 1) < 1e-9:  # u = 1
                a_n += n + 1
            elif abs(u_val + 1) < 1e-9:  # u = -1
                a_n += n
            else:  # |u| < 1
                a_n += 2*n
        
        sum_a += a_n
    
    return sum_a

result = verify()
if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")