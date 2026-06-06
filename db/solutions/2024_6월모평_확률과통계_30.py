from sympy import Rational
from math import comb

def solve(
    white_numbers=[1, 2, 3, 4],
    black_numbers=[4, 5, 6, 7],
    different_color_score=12,
    max_score=24
):
    """
    주머니에서 공 2개를 꺼낼 때 점수가 max_score 이하의 짝수일 확률의 분모+분자를 반환
    
    Args:
        white_numbers: 흰 공의 숫자 리스트 (기본값: [1,2,3,4])
        black_numbers: 검은 공의 숫자 리스트 (기본값: [4,5,6,7])
        different_color_score: 서로 다른 색 공을 꺼냈을 때의 점수 (기본값: 12)
        max_score: 조건의 최대 점수 (기본값: 24)
    
    Returns:
        확률 a/b의 분자 a와 분모 b가 기약분수일 때, a+b
    """
    
    def is_valid_score(score):
        """점수가 짝수이고 max_score 이하인지 확인"""
        return score % 2 == 0 and score <= max_score
    
    # Case 1: 서로 다른 색 (흰 공 1개 × 검은 공 1개)
    different_color_count = 0
    if is_valid_score(different_color_score):
        different_color_count = len(white_numbers) * len(black_numbers)
    
    # Case 2: 같은 색 (흰 공 2개)
    same_white_count = 0
    for i in range(len(white_numbers)):
        for j in range(i + 1, len(white_numbers)):
            product = white_numbers[i] * white_numbers[j]
            if is_valid_score(product):
                same_white_count += 1
    
    # Case 3: 같은 색 (검은 공 2개)
    same_black_count = 0
    for i in range(len(black_numbers)):
        for j in range(i + 1, len(black_numbers)):
            product = black_numbers[i] * black_numbers[j]
            if is_valid_score(product):
                same_black_count += 1
    
    # 전체 경우의 수: 전체 공 중 2개를 동시에 꺼냄
    total_balls = len(white_numbers) + len(black_numbers)
    total = comb(total_balls, 2)
    
    # 조건을 만족하는 경우의 수
    favorable = different_color_count + same_white_count + same_black_count
    
    # 확률을 기약분수로 표현
    prob = Rational(favorable, total)
    a = prob.p  # 분자
    b = prob.q  # 분모
    
    # a + b 반환
    return a + b


CANDIDATE = 51
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')