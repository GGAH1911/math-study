from sympy import symbols, Abs, limit, oo, solve, diff

CANDIDATE = 24

def verify():
    """
    원래 문제의 조건으로 CANDIDATE를 검증한다.
    
    함수 정의:
    - 외부: f(x) = |ax - 4| / |x - b|  (x < 4/a 또는 x > b)
    - 내부: f(x) = ax² - 4bx  (4/a ≤ x ≤ b)
    
    조건:
    - (가) f는 일대일함수
    - (나) p × m = -64
      * p: f(x) = k의 해가 존재하지 않는 양수 k
      * m: [4/a, b]에서 f의 최솟값
    """
    
    # 조건을 만족하는 두 순서쌍
    pairs = [(2, 4), (-1, -3)]
    
    for a, b in pairs:
        x = symbols('x', real=True)
        
        # 경계값
        boundary = 4 / a
        
        # 기본 조건: b > 4/a
        if not (b > boundary):
            print("VERIFY_FAIL")
            return
        
        # 외부 함수: g(x) = |ax - 4| / |x - b|
        # x → ±∞에서 |a|로 수렴 → p = |a|
        g = Abs(a*x - 4) / Abs(x - b)
        p = float(limit(g, x, oo))
        
        # 내부 함수: h(x) = ax² - 4bx on [4/a, b]
        h = a*x**2 - 4*b*x
        
        # h의 값: 끝점과 임계점에서의 값
        h_vals = [float(h.subs(x, boundary)), float(h.subs(x, b))]
        
        # 임계점 (h'(x) = 0에서)
        h_prime = diff(h, x)  # = 2ax - 4b
        for cp in solve(h_prime, x):
            cp_float = float(cp)
            # 임계점이 구간 [4/a, b] 내에 있으면 값 추가
            if boundary <= cp_float <= b:
                h_vals.append(float(h.subs(x, cp_float)))
        
        m = min(h_vals)  # 최솟값
        h_max = max(h_vals)
        
        # 조건 (나) 검증: p × m = -64
        if abs(p * m - (-64)) > 1e-9:
            print("VERIFY_FAIL")
            return
        
        # 조건 (가) 검증: 일대일함수
        # 내부 치역 [m, h_max]와 외부 치역 (0, p) ∪ (p, ∞)이 겹치지 않아야 함
        # → h_max < 0 또는 m > p 중 하나가 참
        if not (h_max < 0 or m > p):
            print("VERIFY_FAIL")
            return
    
    # 모든 순서쌍이 조건을 만족 → a₁×b₁×a₂×b₂ 계산
    product = 2 * 4 * (-1) * (-3)
    
    if product == CANDIDATE:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")

verify()