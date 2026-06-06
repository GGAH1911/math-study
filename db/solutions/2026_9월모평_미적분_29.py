from sympy import Rational, gcd, divisors

def solve(product=216, bound=10):
    """
    파라미터 솔버: 등비수열의 정수항 조건으로부터 답 계산
    
    params:
    - product: 정수항 3개의 곱 (기본값: 216)
    - bound: 조건 (가) a_1 + a_2 < bound의 상한 (기본값: 10)
    
    returns: p + q (무한급수 합 = q/p, 기약분수)
    """
    
    def find_integer_cbrt(n):
        """n의 정수 세제곱근을 찾기"""
        if n == 0:
            return 0
        sign = 1 if n > 0 else -1
        n_abs = abs(n)
        x = round(n_abs ** (1/3))
        # 부동소수점 오차 처리
        for candidate in [x - 1, x, x + 1]:
            if candidate >= 0 and candidate ** 3 == n_abs:
                return sign * candidate
        return None
    
    # 정수항 3개 (A, B, C)에서:
    # B^2 = AC (기하수열 성질)
    # ABC = product
    # => B^3 = product
    B = find_integer_cbrt(product)
    if B is None or B == 0:
        return None
    
    AC = B * B
    
    # (A, C) 쌍 찾기: AC = B^2를 만족하는 모든 정수쌍
    candidates = []
    for d in divisors(abs(AC)):
        for sign_A in [1, -1]:
            A = sign_A * d
            if AC % A == 0:
                C = AC // A
                r = Rational(C, B)
                # 급수 수렴 조건: |r| < 1
                if abs(r) < 1:
                    candidates.append((A, B, C, r))
    
    # 중복 제거
    candidates = list(set(candidates))
    
    valid_results = []
    
    for A, B, C, r in candidates:
        # 정수항이 n_1, n_1+1, n_1+2번째인 경우들
        for n_1 in range(1, 100):
            # a_1 = A * r^(-(n_1-1))
            a_1 = A * (r ** (-(n_1 - 1)))
            
            # 조건 1: a_1 > 0 (첫째항이 양수)
            if a_1 <= 0:
                continue
            
            # 조건 2: a_1 + a_2 < bound
            a_2 = a_1 * r
            if a_1 + a_2 >= bound:
                continue
            
            # 조건 3: 정수항이 정확히 3개, 연속인지 확인
            integer_indices = []
            for n in range(1, 500):
                a_n = a_1 * (r ** (n - 1))
                if a_n.is_integer:
                    integer_indices.append(n)
                # 3개 초과하면 중단
                if len(integer_indices) > 3:
                    break
            
            # 정수항이 정확히 3개이고 연속?
            if len(integer_indices) != 3 or integer_indices != [n_1, n_1 + 1, n_1 + 2]:
                continue
            
            # 무한급수의 합: sum = a_1 / (1 - r)
            sum_inf = a_1 / (1 - r)
            
            # 기약분수 표현: sum = q / p
            q_val = sum_inf.p  # numerator
            p_val = sum_inf.q  # denominator
            
            # p와 q가 서로소인지 확인
            if gcd(p_val, q_val) == 1:
                result = p_val + q_val
                valid_results.append(result)
    
    if valid_results:
        return valid_results[0]
    
    return None

# 검증
CANDIDATE = 91
result = solve()
if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')