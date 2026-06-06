from sympy import factorial, binomial

def solve(num_colors=2, num_letters=4, select_count=4):
    """
    색이 num_colors개(예: 흰색, 검은색), 문자가 num_letters개(예: A, B, C, D),
    각 (색, 문자) 조합마다 1개 원판씩 있을 때,
    총 num_colors*num_letters개 중 select_count개를 선택해 원기둥 모양으로 배치하는 경우의 수.
    
    규칙 (가): 선택된 원판 중 같은 문자가 2개 이상이면, 검은색이 흰색보다 아래.
    규칙 (나): 선택된 원판이 모두 다른 문자이면, num_letters번째 문자가 맨 아래.
    
    파라미터:
    - num_colors: 색 종류 (기본값 2: 흰색, 검은색)
    - num_letters: 문자 종류 (기본값 4: A, B, C, D)
    - select_count: 선택할 원판 개수 (기본값 4)
    
    반환: 경우의 수 (정수)
    """
    
    total = 0
    
    # p: 같은 문자 쌍의 개수 (같은 문자가 정확히 2개인 경우)
    max_pairs = min(select_count // 2, num_letters)
    
    for p in range(max_pairs + 1):
        single_count = select_count - 2 * p  # 단독 문자 개수
        
        # 단독 문자가 가능한 개수를 초과하면 불가능
        if single_count < 0 or single_count > num_letters - p:
            continue
        
        # === 선택 (색깔 조합 포함) ===
        # 1. 쌍을 이룰 p개 문자 선택
        ways_pair_letters = binomial(num_letters, p)
        
        # 2. 나머지 문자 중 단독으로 선택할 single_count개 선택
        ways_single_letters = binomial(num_letters - p, single_count)
        
        # 3. 단독 문자 각각의 색 선택
        ways_single_colors = 2 ** single_count
        
        # 선택 총 가짓수
        ways_select = ways_pair_letters * ways_single_letters * ways_single_colors
        
        # === 배치 (순서 배열) ===
        if p == 0 and select_count == num_letters:
            # 규칙 (나): num_letters번째 문자가 맨 아래 고정
            ways_arrange = factorial(select_count - 1)
        else:
            # 규칙 (가): p개 쌍, 각 쌍의 검은색이 흰색 아래 고정
            ways_arrange = factorial(select_count) // (2 ** p)
        
        # 이 경우의 수를 합산
        total += ways_select * ways_arrange
    
    return int(total)


CANDIDATE = 708
result = solve()
print('VERIFY_PASS' if result == CANDIDATE else f'VERIFY_FAIL: got {result}')