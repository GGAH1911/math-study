from math import isclose

CANDIDATE = 11

def verify():
    """
    원래 문제의 조건:
    - f(x) = |p*sin(x) - q|, 자연수 p, 실수 q >= 0
    - 조건 (나): max f(x) = 15
    - 조건 (가): f(a) = q인 양수 a들을 정렬했을 때 a_1, a_4, a_7이 등차수열
    
    분석 과정:
    1. 조건 (나)에서 max f(x) = max(p+q, |p-q|) = p+q = 15
       => q = 15-p, p ∈ {1,2,...,15}
    
    2. 조건 (가)에서 f(a) = q
       => |p*sin(a) - q| = q
       => p*sin(a) = 0 또는 p*sin(a) = 2q
       => sin(a) = 0 또는 sin(a) = 2q/p = k
    
    3. k = 2q/p = 2(15-p)/p로 놓고 경우 분석:
    
       경우 1: k > 1 (즉 p ∈ {1,...,9})
       - sin(a) = k > 1은 불가능
       - sin(a) = 0만 가능 => a_n = n*π
       - a_1 = π, a_4 = 4π, a_7 = 7π
       - 공차: 4π - π = 3π, 7π - 4π = 3π => 등차수열 ✓
       - 9개 쌍
    
       경우 2: k = 1 (즉 p = 10, q = 5)
       - sin(a) = 0 또는 sin(a) = 1
       - sin(a) = 0: a = n*π
       - sin(a) = 1: a = π/2 + 2m*π
       - 정렬: π/2, π, 2π, 5π/2, 3π, 4π, 9π/2, ...
       - a_1 = π/2, a_4 = 5π/2, a_7 = 9π/2
       - 공차: 5π/2 - π/2 = 2π, 9π/2 - 5π/2 = 2π => 등차수열 ✓
       - 1개 쌍
    
       경우 3: 0 < k < 1 (즉 p ∈ {11,12,13,14})
       - sin(a) = 0 또는 sin(a) = k ∈ (0,1)
       - α = arcsin(k) ∈ (0, π/2)일 때
       - 정렬: α, π-α, π, 2π, 2π+α, 3π-α, 3π, ...
       - a_1 = α, a_4 = 2π, a_7 = 3π
       - 등차조건: 2(2π) = α + 3π => α = π (불가능, α < π/2) ✗
       - 0개 쌍
    
       경우 4: k = 0 (즉 p = 15, q = 0)
       - sin(a) = 0만 가능 => a_n = n*π
       - a_1 = π, a_4 = 4π, a_7 = 7π
       - 공차 = 3π => 등차수열 ✓
       - 1개 쌍
    
    총 개수: 9 + 1 + 0 + 1 = 11
    """
    
    valid_count = 0
    
    for p in range(1, 16):
        q = 15 - p
        
        if q < 0:
            continue
        
        # 조건 (나): p + q = 15 확인
        assert p + q == 15, f"Condition (나) failed: p={p}, q={q}"
        
        # k = 2q/p = 2(15-p)/p
        k = 2 * q / p
        
        # 경우 1: k > 1
        if k > 1:
            # sin(a) = 0만 가능 => a_n = n*π
            # a_1 = π, a_4 = 4π, a_7 = 7π (공차 3π) => 등차수열
            valid_count += 1
        
        # 경우 2: k = 1
        elif isclose(k, 1.0):
            # sin(a) = 0 또는 sin(a) = 1
            # a_1 = π/2, a_4 = 5π/2, a_7 = 9π/2 (공차 2π) => 등차수열
            valid_count += 1
        
        # 경우 3: 0 < k < 1
        elif 0 < k < 1:
            # a_1 = α, a_4 = 2π, a_7 = 3π
            # 등차조건 위반 => 불만족
            pass
        
        # 경우 4: k = 0
        elif isclose(k, 0.0):
            # sin(a) = 0만 가능 => a_n = n*π
            # a_1 = π, a_4 = 4π, a_7 = 7π (공차 3π) => 등차수열
            valid_count += 1
    
    return valid_count


result = verify()

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {CANDIDATE}, got {result}")