"""2026 고2 6월 단일 06 (지수로그, 객관식)
f(x)=log_2(x-3)+5, 4<=x<=11 의 최댓값+최솟값. 증가함수 → f(4)+f(11)=5+8=13=보기②."""
import sympy as sp

CANDIDATE = 2
choices = {1: 11, 2: 13, 3: 15, 4: 17, 5: 19}


def solve(lo=4, hi=11, shift=3, const=5):
    # f(x)=log_2(x-shift)+const, 정의역에서 증가 → 최소 f(lo), 최대 f(hi)
    f = lambda x: sp.log(x - shift, 2) + const
    val = sp.nsimplify(f(lo) + f(hi))
    for num, cval in choices.items():
        if sp.simplify(val - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
