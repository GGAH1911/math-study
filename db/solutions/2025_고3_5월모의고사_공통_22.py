from fractions import Fraction
from math import gcd
import sympy as sp

CANDIDATE = 71

def main():
    x = sp.Symbol('x', real=True)
    
    # Step 1: f(f(x)) = x의 모든 해를 구한다
    # 이들이 가능한 a₃ 값들이다
    a3_candidates = set()
    
    # Case 1: x ≤ 0 ⟹ f(x) = x², f(f(x)) = -2x² + 3 = x
    # 2x² + x - 3 = 0 ⟹ x = -3/2 또는 x = 1
    # x ≤ 0만 취함: x = -3/2
    sols = sp.solve(2*x**2 + x - 3, x)
    a3_candidates.update(s for s in sols if s <= 0)
    
    # Case 2: 0 < x < 3/2 ⟹ f(x) = -2x + 3, f(f(x)) = 4x - 3 = x
    # x = 1 ✓
    a3_candidates.add(sp.Integer(1))
    
    # Case 3: x ≥ 3/2 ⟹ f(x) = -2x + 3 ≤ 0
    # f(f(x)) = (-2x+3)² = x ⟹ 4x² - 13x + 9 = 0
    # x ≥ 3/2만 취함: x = 9/4
    sols = sp.solve(4*x**2 - 13*x + 9, x)
    a3_candidates.update(s for s in sols if s >= sp.Rational(3, 2))
    
    # Case 4: x = 0은 고정점
    a3_candidates.add(sp.Integer(0))
    
    # Step 2-4: 각 a₃에 대해 역으로 a₂, a₁ 찾기
    valid_a1_list = []
    
    for a3 in a3_candidates:
        y = sp.Symbol('y', real=True)
        
        # f(a₂) = a₃를 풀기
        a2_candidates = []
        
        # Sub-case A: a₂ ≤ 0 ⟹ a₂² = a₃
        if a3 >= 0:
            sols_a2 = sp.solve(y**2 - a3, y)
            a2_candidates.extend(s for s in sols_a2 if s <= 0)
        
        # Sub-case B: a₂ > 0 ⟹ -2a₂ + 3 = a₃
        sols_a2 = sp.solve(-2*y + 3 - a3, y)
        a2_candidates.extend(s for s in sols_a2 if s > 0)
        
        for a2 in a2_candidates:
            # f(a₁) = a₂를 풀기
            a1_candidates = []
            
            # Sub-case A: a₁ ≤ 0 ⟹ a₁² = a₂
            if a2 >= 0:
                sols_a1 = sp.solve(y**2 - a2, y)
                a1_candidates.extend(s for s in sols_a1 if s <= 0)
            
            # Sub-case B: a₁ > 0 ⟹ -2a₁ + 3 = a₂
            sols_a1 = sp.solve(-2*y + 3 - a2, y)
            a1_candidates.extend(s for s in sols_a1 if s > 0)
            
            for a1 in a1_candidates:
                # 조건 확인: (가) a₁ × a₂ > 0, a₁ ∈ (0, 3/2)
                if a1 * a2 > 0 and 0 < a1 < sp.Rational(3, 2):
                    valid_a1_list.append(a1)
    
    # Step 5: 모든 유효한 a₁의 합
    total_sum = sum(valid_a1_list)
    
    # 기약분수로 변환
    total_frac = sp.nsimplify(total_sum)
    
    # q/p 형식에서
    numerator, denominator = total_frac.as_numer_denom()
    q_val, p_val = int(numerator), int(denominator)
    
    # gcd 확인
    g = gcd(p_val, q_val)
    
    # p + q 계산
    result = p_val + q_val
    
    # 검증: CANDIDATE와 일치하고 기약분수여야 함
    if result == CANDIDATE and g == 1:
        return 'VERIFY_PASS'
    else:
        return 'VERIFY_FAIL'

print(main())