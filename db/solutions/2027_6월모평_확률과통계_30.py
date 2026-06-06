from sympy import binomial

def solve(yellow=4, purple=4, black=4):
    """
    노란색, 보라색, 검은색 공을 일렬로 배열할 때,
    노란색 공이 보라색 공과 이웃하지 않는 경우의 수.
    
    Parameters:
    - yellow: 노란색 공 개수 (기본값 4)
    - purple: 보라색 공 개수 (기본값 4)
    - black: 검은색 공 개수 (기본값 4)
    
    Returns:
    - 조건을 만족하는 배열의 경우의 수 (정수)
    
    풀이:
    검은색 black개를 배치하면 (black+1)개의 간격이 생긴다.
    각 비어있지 않은 간격을 Y 또는 P로만 배정하되,
    Y 합 = yellow, P 합 = purple을 만족해야 한다.
    포함-배제 원리 공식:
    sum_{k=0}^{b} (-1)^k * C(b+1, k) * C(y+p-k, y)^2
    """
    b = black
    y = yellow
    p = purple
    
    # 포함-배제 공식 계산
    result = 0
    for k in range(b + 1):
        term = ((-1)**k 
                * binomial(b + 1, k) 
                * binomial(y + p - k, y)**2)
        result += term
    
    return result

CANDIDATE = 780
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')