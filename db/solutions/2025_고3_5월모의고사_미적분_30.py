from sympy import Rational, simplify, symbols, solve as sp_solve

def solve(r=3, coeff_b5=81, coeff_b6=243, const_term=Rational(9, 4), rhs_cond_na=90):
    """
    한국 수능 수학 - 등비수열과 조건식 parametric solver
    
    파라미터:
    - r: 등비수열의 공비 (기본값: 3)
    - coeff_b5: b_5의 계수, 즉 b_5 = coeff_b5 * a (기본값: 81 = 3^4)
    - coeff_b6: b_6의 계수, 즉 b_6 = coeff_b6 * a (기본값: 243 = 3^5)
    - const_term: 관계식 우변의 상수항 (기본값: 9/4)
    - rhs_cond_na: 조건 (나)의 우변값 → 최종 답에 곱하는 계수 (기본값: 90)
    
    핵심 관계식: (coeff_b5 * a)^2 = coeff_b6 * a - const_term
    최종 계산: result = rhs_cond_na * a_3, where a_3 = a * r^2
    """
    
    a = symbols('a', positive=True, real=True)
    
    # 이차방정식: (coeff_b5 * a)^2 = coeff_b6 * a - const_term
    # 정리: coeff_b5^2 * a^2 - coeff_b6 * a + const_term = 0
    
    eq = coeff_b5**2 * a**2 - coeff_b6 * a + const_term
    solutions = sp_solve(eq, a)
    
    if not solutions:
        return None
    
    # 양수 해 선택 (모든 항이 양수인 등비수열 조건)
    positive_sols = [sol for sol in solutions if sol.is_positive]
    if not positive_sols:
        positive_sols = solutions
    
    a_val = positive_sols[0]
    
    # 등비수열의 일반항: a_n = a_1 * r^(n-1)
    # 따라서 a_3 = a * r^2
    a_3 = a_val * r**2
    
    # 조건 (나)의 우변값으로 최종 답 계산
    result = rhs_cond_na * a_3
    
    return simplify(result)


# 정답 검증
CANDIDATE = 15
result = solve()
print('VERIFY_PASS' if simplify(result - CANDIDATE) == 0 else 'VERIFY_FAIL')