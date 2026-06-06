from sympy import pi, simplify

def solve(coeff=10, limit_numerator_coeff=1):
    """
    함수 y = sqrt(x)/coeff 와 y = tan(x) 의 교점 극한 문제
    
    a_n: 두 함수의 교점의 x좌표 (작은 순서)
    
    구하는 값: lim_{n→∞} (limit_numerator_coeff/π²) × a_n³ tan²(a_{n+1}-a_n)
    
    점근 분석:
    - 각 구간 [kπ, kπ+π/2) 에서 교점 c_k 존재
    - c_k = kπ + π/2 - δ_k, 여기서 δ_k ≈ coeff/√(kπ)
    - a_n ≈ nπ (큰 n에 대해)
    - a_{n+1} - a_n ≈ π + coeff/(2√π n^{3/2})
    - tan(a_{n+1} - a_n) ≈ coeff/(2√π n^{3/2})
    - a_n³ ≈ n³π³
    - a_n³ tan²(a_{n+1} - a_n) ≈ coeff² π²/4
    
    따라서:
    (limit_numerator_coeff/π²) × coeff² π²/4 = limit_numerator_coeff × coeff²/4
    """
    
    # 점근값: coeff² π²/4
    limit_value = coeff**2 * pi**2 / 4
    
    # 최종 극한값
    result = simplify((limit_numerator_coeff / pi**2) * limit_value)
    
    return result

# 원문제 검증
CANDIDATE = 25
print('VERIFY_PASS' if solve(coeff=10, limit_numerator_coeff=1) == CANDIDATE else 'VERIFY_FAIL')