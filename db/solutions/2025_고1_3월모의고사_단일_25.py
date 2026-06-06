from sympy import divisors

def solve(volume=33, sum_divisor=7):
    """
    직육면체의 겉넓이를 구하는 함수
    
    Parameters:
    - volume: 직육면체의 부피 (a*b*c = volume)
    - sum_divisor: a+b+c가 배수여야 할 수
    
    Returns:
    - 겉넓이 (2(ab + bc + ca))
    """
    
    # volume의 약수 구하기
    div_list = list(divisors(volume))
    
    valid_solutions = []
    
    # 조건을 만족하는 모든 (a, b, c) 찾기
    for a in div_list:
        for b in div_list:
            if volume % (a * b) == 0:
                c = volume // (a * b)
                
                # 부피 조건과 합 조건 확인
                if a * b * c == volume and (a + b + c) % sum_divisor == 0:
                    valid_solutions.append((a, b, c))
    
    # 첫 번째 유효한 해의 겉넓이 계산
    if valid_solutions:
        a, b, c = valid_solutions[0]
        # 겉넓이 = 2(ab + bc + ca)
        surface_area = 2 * (a*b + b*c + c*a)
        return surface_area
    
    return None

CANDIDATE = 134
result = solve()
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')