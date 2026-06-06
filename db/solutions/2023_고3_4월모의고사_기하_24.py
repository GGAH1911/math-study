"""2023 고3 4월 기하 24 (이차곡선, 객관식)
쌍곡선 x²/a² - y²/b²=1 (b²=8), 점근선 y=√2 x → b/a=√2 → a=2.
c²=a²+b²=12, 두 초점거리 2c=4√3=보기⑤."""
import sympy as sp

CANDIDATE = 5
choices = {1: 4 * sp.sqrt(2), 2: sp.Integer(6), 3: 2 * sp.sqrt(10), 4: 2 * sp.sqrt(11), 5: 4 * sp.sqrt(3)}


def solve(b2=8, slope_sq=2):
    # 점근선 기울기 b/a=√slope_sq → a²=b²/slope_sq
    a2 = sp.Rational(b2, 1) / slope_sq
    c = sp.sqrt(a2 + b2)
    val = sp.simplify(2 * c)                     # 두 초점 사이 거리
    for num, cval in choices.items():
        if sp.simplify(val - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
