from fractions import Fraction
from itertools import combinations

def verify():
    # y가 처음으로 3이 되는 모든 경우
    total_prob_y_eq_3 = Fraction(0)
    prob_x_eq_1_y_eq_3 = Fraction(0)
    
    # x=0: BBB
    prob = Fraction(1, 2) ** 3
    total_prob_y_eq_3 += prob
    
    # x=1: 처음 3번(H 1개, B 2개) + 마지막 B
    for pos in range(3):
        prob = Fraction(1, 2) ** 4
        total_prob_y_eq_3 += prob
        prob_x_eq_1_y_eq_3 += prob
    
    # x=2: 처음 4번(H 2개, B 2개) + 마지막 B
    for combo in combinations(range(4), 2):
        prob = Fraction(1, 2) ** 5
        total_prob_y_eq_3 += prob
    
    # 조건부 확률
    result = prob_x_eq_1_y_eq_3 / total_prob_y_eq_3
    
    if result == Fraction(3, 8):
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: {result}')

verify()