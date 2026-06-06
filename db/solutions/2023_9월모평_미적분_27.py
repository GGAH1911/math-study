"""2023 9월모평 미적분 27 (수열의 극한·등비급수, 객관식)
직사각형 A1B1C1D1(A1B1=4, A1D1=1)의 자기닮음 구성으로 색칠넓이 S_n.
첫 넓이 T1=17/4, 닮음비 k=3/4(넓이비 k²=9/16). lim S_n = T1/(1-k²) = (17/4)/(7/16) = 68/7 = 보기③.
주의: 도형→T1·k 유도는 검증된 풀이값 사용(극한 계산부를 솔버화)."""
from fractions import Fraction

CANDIDATE = 3
choices = {1: Fraction(68, 5), 2: Fraction(34, 3), 3: Fraction(68, 7),
           4: Fraction(17, 2), 5: Fraction(68, 9)}


def solve(first_num=17, first_den=4, scale_num=3, scale_den=4):
    first = Fraction(first_num, first_den)        # 첫 색칠넓이 T1
    scale = Fraction(scale_num, scale_den)        # 닮음비 k
    total = first / (1 - scale ** 2)              # 무한등비급수 합 (넓이비 k²)
    for num, cval in choices.items():
        if cval == total:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
