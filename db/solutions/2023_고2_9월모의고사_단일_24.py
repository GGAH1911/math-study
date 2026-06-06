from sympy import log, simplify, N

def solve(coeff=6, base=3, x_offset=2, x_min=1, x_max=25):
    """
    함수 f(x) = coeff * log_base(x + x_offset)의
    정의역 [x_min, x_max]에서의 최댓값 M과 최솟값 m의 합을 계산한다.
    
    이 함수는 단조증가이므로:
    - 최솟값 m = f(x_min)
    - 최댓값 M = f(x_max)
    
    Parameters:
    - coeff: 로그 앞의 계수 (기본값: 6)
    - base: 로그의 밑 (기본값: 3)
    - x_offset: x 내부의 상수항 (기본값: 2)
    - x_min: 정의역 최솟값 (기본값: 1)
    - x_max: 정의역 최댓값 (기본값: 25)
    """
    m = coeff * log(x_min + x_offset, base)
    M = coeff * log(x_max + x_offset, base)
    result = simplify(M + m)
    answer = int(N(result))
    return answer

CANDIDATE = '24'
answer = solve()
print('VERIFY_PASS' if str(answer) == CANDIDATE else 'VERIFY_FAIL')