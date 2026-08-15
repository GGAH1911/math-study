"""
확률변수 X = 앞뒤 숫자가 다른 카드 개수, E(X) 문제 파라미터화 솔버

[문제 구조]
상자에 카드 1..N 이 들어 있다. 이 중 n 장을 순서대로(비복원) 뽑아 뒷면에
1,2,...,n 을 차례로 적는다. i번째로 뽑은 카드의 앞면 숫자가 i(=뒷면 숫자)와
같으면 "일치", 다르면 "불일치"이고, X = 불일치 카드의 개수(확률변수)이다.
X 가 가질 수 있는 값은 0..n 이며, 순열 전체 경우의 수는 P(N,n)=N!/(N-n)!.

원문제(N=5,n=3)는 P(X=1)=a, P(X=2)=b, E(X)=c 를 구해
10a+20b+5c 의 값(=20, 보기 ①)을 묻는다.

[파라미터]
  N       : 상자 속 전체 카드 수 (원문제 5)
  n       : 뽑아서 뒷면 번호를 매기는 카드 수 (원문제 3)
  w1,w2,w3: P(X=1), P(X=2), E(X) 을 결합하는 계수 (원문제 10,20,5)
  → N, w3 는 값을 바꾸면 보기 번호(정답 위치)까지 실제로 바뀐다(아래 확인).

[보기 생성 구조]
원문제 보기 20,24,28,32,36 은 정답 V=20 을 기준으로 공차 4(=240/T, T=60)인
등차수열이며 정답이 그 1번째(①)이다. 이를 일반화해, 정수
  S = w1*count(X=1) + w2*count(X=2) + w3*Σ k·count(X=k)   (count 는 순열 개수, 정수)
가 240 의 배수일 때만 "깔끔한 문제"로 보고, S/240 을 5로 나눈 나머지로 정답의
보기 위치(①~⑤)를 정하며, 그 위치를 포함하도록 공차 240/T 인 등차수열 5개를
보기로 만든다(원문제에서는 이 공차가 정확히 4). 배수가 아니면(깔끔한 5지선다
문제가 되지 않으면) 예외를 던진다.
"""
import itertools
import sympy as sp

CANDIDATE = 1  # 원문제 정답: ① (절대 바꾸지 않음)

PARAMS = dict(N=5, n=3, w1=10, w2=20, w3=5)

_GRID = 240  # 원문제의 보기 공차(4) × 기준 경우의 수(P(5,3)=60)


def _counts(N, n):
    """뽑은 n장의 순서열 중, 불일치 개수(X)별 경우의 수를 실제로 세어 구한다."""
    N, n = int(N), int(n)
    if N < 1 or n < 1 or n > N:
        raise ValueError('N >= n >= 1 이어야 한다')
    cnt = [0] * (n + 1)
    for perm in itertools.permutations(range(1, N + 1), n):
        matches = sum(1 for i in range(n) if perm[i] == i + 1)
        cnt[n - matches] += 1
    return cnt


def _S_T(prm):
    """정수 S(=가중합의 분자)와 총 경우의 수 T(=P(N,n))를 구한다."""
    N, n = prm['N'], prm['n']
    w1, w2, w3 = prm['w1'], prm['w2'], prm['w3']
    cnt = _counts(N, n)
    T = 1
    for i in range(int(n)):
        T *= (int(N) - i)
    EXnum = sum(k * cnt[k] for k in range(len(cnt)))       # Σ k·count(X=k)
    cnt1 = cnt[1] if len(cnt) > 1 else 0
    cnt2 = cnt[2] if len(cnt) > 2 else 0
    S = w1 * cnt1 + w2 * cnt2 + w3 * EXnum
    return S, T


def value(prm):
    """w1*P(X=1) + w2*P(X=2) + w3*E(X) 의 실제 값(sympy 유리수)."""
    S, T = _S_T(prm)
    return sp.Rational(S, T)


def choices(prm):
    """값 V를 포함하도록, S가 240의 배수라는 조건에서 유도한 5지선다 보기.
    공차는 240/T 이며 원문제(T=60)에서는 정확히 4가 되어 (20,24,28,32,36)과 일치한다."""
    S, T = _S_T(prm)
    if S % _GRID != 0:
        raise ValueError(f'S={S} 가 {_GRID}의 배수가 아니라 보기가 깔끔하게 정해지지 않는다')
    q = S // _GRID
    offset = q % 5
    S0 = S - offset * _GRID
    return [sp.Rational(S0 + i * _GRID, T) for i in range(5)]


def solve(prm):
    """조건 → 보기 번호(①=1 ... ⑤=5)."""
    V = value(prm)
    ch = choices(prm)
    return ch.index(V) + 1


def statement(prm):
    N, n = prm['N'], prm['n']
    w1, w2, w3 = prm['w1'], prm['w2'], prm['w3']
    ch = choices(prm)
    labels = '①②③④⑤'
    opts = ' '.join(f'{labels[i]} {sp.nsimplify(c)}' for i, c in enumerate(ch))
    return (
        f'앞면에 숫자 1부터 {N}까지 하나씩 적혀 있는 {N}장의 카드가 상자에 들어 있다. '
        f'이 상자에서 임의로 {n}장의 카드를 한 장씩 꺼내고, 꺼낸 순서대로 카드의 뒷면에 '
        f'숫자 1, 2, ..., {n}을 차례로 적는다. 이 {n}장의 카드 중 앞뒤 양쪽 면에 서로 다른 '
        f'숫자가 적혀 있는 카드의 개수를 확률변수 X라 하자. P(X=1)=a, P(X=2)=b, E(X)=c라 '
        f'할 때, {w1}a+{w2}b+{w3}c 의 값은?\n{opts}'
    )


# 유도한 보기가 원문제 보기(① 20 ② 24 ③ 28 ④ 32 ⑤ 36)와 같은지 고정
assert choices(PARAMS) == [20, 24, 28, 32, 36], choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
