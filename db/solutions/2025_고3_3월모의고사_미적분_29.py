from sympy import *

CANDIDATE = 13

def verify_solution():
    """원 O, 점 A,B,D,E와 주어진 모든 조건으로부터 답을 검증"""
    
    # 자연수 n (n ≥ 2)
    n = symbols('n', positive=True, integer=True)
    
    # 원의 중심 C = (0, 0), 반지름 = n
    # 조건: AB = 2를 만족하는 원 위의 두 점 A, B
    C = Matrix([0, 0])
    A = Matrix([-1, -sqrt(n**2 - 1)])
    B = Matrix([1, -sqrt(n**2 - 1)])
    
    # 검증 1: |AB| = 2
    AB = sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
    if simplify(AB - 2) != 0:
        return False
    
    # 검증 2: A, B가 반지름 n인 원 위의 점
    CA = sqrt(A[0]**2 + A[1]**2)
    CB = sqrt(B[0]**2 + B[1]**2)
    if simplify(CA - n) != 0 or simplify(CB - n) != 0:
        return False
    
    # 점 D: ∠BAC를 이등분하는 직선과 원의 교점 (A 제외)
    D = Matrix([n, 0])
    
    # 검증 3: D가 원 위의 점
    CD = sqrt(D[0]**2 + D[1]**2)
    if simplify(CD - n) != 0:
        return False
    
    # 점 E: 호 AD (B 미포함) 위의 점, BD:DE = √2:1
    E = Matrix([(n+1)/2, sqrt((n-1)*(3*n+1))/2])
    
    # 검증 4: E가 원 위의 점
    CE = sqrt(E[0]**2 + E[1]**2)
    if simplify(CE - n) != 0:
        return False
    
    # 검증 5: BD:DE = √2:1 조건
    BD = sqrt((D[0] - B[0])**2 + (D[1] - B[1])**2)
    DE = sqrt((E[0] - D[0])**2 + (E[1] - D[1])**2)
    if simplify(BD / DE - sqrt(2)) != 0:
        return False
    
    # 삼각형 CDE의 넓이
    # C(0,0), D(n,0), E((n+1)/2, √((n-1)(3n+1))/2)
    # 넓이 = (1/2)|n·√((n-1)(3n+1))/2| = n√((n-1)(3n+1))/4
    S_n = n * sqrt((n-1)*(3*n+1)) / 4
    
    # 극한값 검증: lim_{n→∞} ((√3/4)n - S_n/n) = (q/p)√3
    expr = sqrt(3)/4 * n - S_n/n
    lim = limit(expr, n, oo)
    
    # 예상 극한값: √3/12
    expected = sqrt(3) / 12
    if simplify(lim - expected) != 0:
        return False
    
    # 극한값 = (q/p)√3 에서 q/p = 1/12
    # p=12, q=1 (서로소인 자연수)
    p, q = 12, 1
    if gcd(p, q) != 1:
        return False
    
    # 답: p + q
    answer = p + q
    return answer == CANDIDATE

if verify_solution():
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')