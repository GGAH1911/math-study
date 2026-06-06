"""2022 고3 4월 기하 24 (이차곡선, 객관식)
쌍곡선 x²/9-y²/16=1, 초점 F(c,0)F'(-c,0), c=√(9+16)=5. |FF'|=2c=10.
조건 |FP|=|FF'|=10. 쌍곡선 정의(우측가지): |PF'|-|PF|=2a=6 → |PF'|=16.
삼각형 PF'F 둘레 = |PF|+|PF'|+|FF'| = 10+16+10 = 36 = 보기②."""
import sympy as sp

CANDIDATE = 2
choices = {1: 35, 2: 36, 3: 37, 4: 38, 5: 39}


def solve(a2=9, b2=16):
    a = sp.sqrt(a2)
    c = sp.sqrt(a2 + b2)
    FF = 2 * c                                   # |FF'|
    FP = FF                                       # 조건 |FP|=|FF'|
    PFp = FP + 2 * a                              # 쌍곡선 정의(우가지): |PF'|=|PF|+2a
    perim = sp.simplify(FP + PFp + FF)
    for num, cval in choices.items():
        if sp.simplify(perim - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
