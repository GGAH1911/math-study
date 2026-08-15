"""2019 고3 4월모의고사 나형 7번 — 파라미터 솔버.

문제 구조: 그래프에서 두 값을 읽어 더한다.
  - f0        : x=0 에서의 함숫값 (채워진 점)
  - right_lim : x→2+ 일 때의 우극한값 (빈 점에서 시작하는 오른쪽 가지의 극한)
  정답값 = f0 + right_lim.

객관식 보기 재현: 실제 수능형 문제의 보기는 "그럴듯한 오답"들로 구성된다.
이 문제 유형의 전형적 오답 패턴을 다음과 같이 모델링한다(그래프에서 또 하나의
단서인 x=2 좌극한값 left_lim 을 추가 파라미터로 둔다):
  - d1 = right_lim              (f(0)을 더하는 것을 잊음)
  - d2 = left_lim                (우극한 대신 좌극한을 읽음)
  - d3 = left_lim + 1            (그래프 눈금을 하나 잘못 읽음)
  - d4 = f0 + left_lim           (우극한 대신 좌극한을 사용해 합을 구함)
정답과 네 오답을 합쳐 5개의 서로 다른 정수가 나오고, 그중 정답의 위치(1~5)가
보기 번호다. f0, right_lim, left_lim 세 파라미터가 값과 보기 구성·정답 위치를
실제로 바꾼다(특히 right_lim, left_lim 은 정답 '보기 번호' 자체를 바꾼다).
"""
import sympy as sp


def value(prm):
    # 그래프의 두 값을 더한다 — 문제의 핵심 수학 구조.
    return sp.Integer(prm['f0']) + sp.Integer(prm['right_lim'])


def choices(prm):
    f0 = sp.Integer(prm['f0'])
    right_lim = sp.Integer(prm['right_lim'])
    left_lim = sp.Integer(prm['left_lim'])
    v = value(prm)
    d1 = right_lim
    d2 = left_lim
    d3 = left_lim + 1
    d4 = f0 + left_lim
    vals = {v, d1, d2, d3, d4}
    if len(vals) != 5:
        raise ValueError(f'보기 5개가 서로 겹침: {sorted(vals)}')
    return sorted(vals)


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1  # 보기 번호(1-based, ①=1 ... ⑤=5)


def statement(prm):
    f0 = prm['f0']
    right_lim = prm['right_lim']
    ch = choices(prm)
    labels = '①②③④⑤'
    opts = ' '.join(f'{labels[i]} {c}' for i, c in enumerate(ch))
    return (
        f"함수 y=f(x)의 그래프가 그림과 같다. 그래프는 x=0에서 채워진 점 (0,{f0})를 지나고, "
        f"x=2에서 왼쪽 가지와 오른쪽 가지가 서로 다른 값으로 접근하며 오른쪽 가지는 x→2+일 때 "
        f"빈 점 (2,{right_lim})으로 접근한다.\n"
        f"f(0) + lim_{{x→2+}} f(x)의 값은?\n{opts}"
    )


PARAMS = dict(
    f0=3,          # 채워진 점 (0,3)
    right_lim=5,   # x→2+ : 빈 점 (2,5)로 접근하는 오른쪽 가지
    left_lim=6,    # x→2- : 좌극한(오답 보기 구성용 추가 단서)
)

CANDIDATE = 4  # 정답 보기 ④ (값 8)

# 원문제 보기가 실제로 ①5 ②6 ③7 ④8 ⑤9 임을 고정 검증
assert choices(PARAMS) == [5, 6, 7, 8, 9]

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
