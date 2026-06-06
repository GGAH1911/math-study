from sympy import pi, sqrt, simplify, Rational

def solve(a=1, b=2*sqrt(6)):
    """
    매개변수 기반 무한급수 합 계산기
    
    Args:
        a: 직사각형 한 변 길이 (기본값 1)
        b: 직사각형 다른 변 길이 (기본값 2√6)
    
    Returns:
        색칠된 부분의 무한 급수 합
    """
    # 1단계: 대각선 길이
    d = sqrt(a**2 + b**2)
    
    # 2단계: S_1 계산
    # S_1 = (1/2)*(theta_1 + theta_2) - (1/4)*(sin(theta_1) + sin(theta_2))
    # theta_1 + theta_2 = π/2 (직각삼각형)
    # sin(theta_1) = b/d, sin(theta_2) = a/d
    S1 = pi/Rational(4) - (a + b)/(4*d)
    
    # 3단계: 닮음비 계산
    k = (d - 2) / d  # B_2D_2 / B_1D_1 = (d-2)/d
    area_ratio = k ** 2  # 넓이비 = (3/5)^2 = 9/25
    
    # 4단계: 무한급수 합
    # Σ S_n = S_1 / (1 - area_ratio)
    result = S1 / (1 - area_ratio)
    
    return simplify(result)

# 검증
CANDIDATE = (25*pi - 10*sqrt(6) - 5) / 64
answer = solve()

if simplify(answer - CANDIDATE) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')