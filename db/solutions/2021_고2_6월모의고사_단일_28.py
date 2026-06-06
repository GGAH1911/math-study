from math import log2

def solve(sum_condition=25, relation_coefficient=3, external_div_p=2):
    """
    완전 파라미터 솔버
    
    파라미터:
    - sum_condition: 집합 합 조건 (기본값 25)
    - relation_coefficient: 관계식 b = coeff*(a+1)의 계수 (기본값 3)
    - external_div_p: 외분 비율 p:1 (기본값 2는 2:1)
    
    반환값: a + b의 최댓값
    """
    
    # 공식: (2p+1) * floor_value + 15 = sum_condition
    # 기본 외분 2:1에서: 5 * floor_value + 15 = sum_condition
    divisor = 2 * external_div_p + 1
    
    if (sum_condition - 15) % divisor != 0:
        return None
    
    floor_value = (sum_condition - 15) // divisor
    
    # floor_value ≤ log₂(b/a) < floor_value + 1
    lower_bound = 2 ** floor_value
    upper_bound = 2 ** (floor_value + 1)
    
    # b = relation_coefficient * (a+1)를 만족하는 자연수 쌍 찾기
    valid_pairs = []
    
    for a in range(1, 10000):
        b = relation_coefficient * (a + 1)
        ratio = b / a
        
        if lower_bound <= ratio < upper_bound:
            valid_pairs.append((a, b))
        elif ratio < lower_bound:
            # a가 증가하면 b/a가 감소하므로 더 이상 조건을 만족할 수 없음
            break
    
    if not valid_pairs:
        return None
    
    # a + b가 최대인 쌍 선택
    best_a, best_b = max(valid_pairs, key=lambda pair: pair[0] + pair[1])
    
    return best_a + best_b


CANDIDATE = 15
result = solve()
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')