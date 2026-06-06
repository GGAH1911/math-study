def solve(target_value=2, threshold=3, alternative=10, target_index=6):
    """
    수열 {a_n}에서 a_{target_index} = target_value가 되는
    모든 자연수 a_1의 합을 구한다.
    
    재귀 관계:
    - a_{n+1} = a_n / n (a_n ≥ threshold)
    - a_{n+1} = alternative (a_n < threshold)
    
    Parameters:
    -----------
    target_value : 목표값 (기본값: 2)
    threshold : 임계값 (기본값: 3)
    alternative : 대체값 (기본값: 10)
    target_index : 목표 인덱스 (기본값: 6)
    
    Returns:
    --------
    int : 조건을 만족하는 모든 자연수 a_1의 합
    """
    from fractions import Fraction
    
    # a_n의 가능한 값들을 역추적
    # 각 원소는 Fraction(특정값) 또는 ('RANGE', Fraction, Fraction)(범위)
    current = {Fraction(target_value)}
    
    # 역추적: target_index -> 1
    for idx in range(target_index - 1, 0, -1):
        next_vals = set()
        
        for val in current:
            if isinstance(val, tuple):
                # Range 처리: ('RANGE', lower, upper)
                _, lower, upper = val
                
                # Case 1: a_idx >= threshold이고 a_idx / idx ∈ [lower, upper)
                # → a_idx ∈ [max(lower*idx, threshold), upper*idx)
                new_lower = max(lower * idx, Fraction(threshold))
                new_upper = upper * idx
                if new_lower < new_upper:
                    next_vals.add(('RANGE', new_lower, new_upper))
                
                # Case 2: a_idx < threshold이고 alternative ∈ [lower, upper)
                if lower <= Fraction(alternative) < upper:
                    next_vals.add(('RANGE', Fraction(0), Fraction(threshold)))
            else:
                # Fraction 처리
                val_frac = Fraction(val)
                
                # Case 1: a_idx >= threshold이고 a_idx / idx = val
                candidate = val_frac * idx
                if candidate >= Fraction(threshold):
                    next_vals.add(candidate)
                
                # Case 2: a_idx < threshold이고 alternative = val
                if val_frac == Fraction(alternative):
                    next_vals.add(('RANGE', Fraction(0), Fraction(threshold)))
        
        current = next_vals
    
    # a_1에서 자연수만 수집
    result = set()
    
    for val in current:
        if isinstance(val, tuple):
            # Range 처리: [lower, upper) ∩ ℤ
            _, lower, upper = val
            
            # 범위의 정수 경계 계산
            if lower.denominator == 1:
                start = int(lower)
            else:
                start = int(lower) + (1 if lower > int(lower) else 0)
            
            if upper.denominator == 1:
                end = int(upper) - 1
            else:
                end = int(upper)
            
            # [start, end] 범위의 자연수 추가
            for n in range(max(1, start), end + 1):
                result.add(n)
        else:
            # Fraction 처리
            if val.denominator == 1 and val >= 1:
                result.add(int(val))
    
    return sum(result)


# 검증
CANDIDATE = 381
if solve() == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')