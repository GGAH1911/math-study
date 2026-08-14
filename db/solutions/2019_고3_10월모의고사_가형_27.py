"""2019 고3 10월모의고사 가형 27번 — 파라미터 솔버.

[문제] 선분 AB를 지름으로 하는 원 위의 점 P에서의 접선과 직선 AB가 만나는 점을 Q라 하자.
점 Q가 선분 AB를 m:n 으로 외분하는 점이고, BQ = ℓ 일 때, AP·AQ (벡터 내적) 의 값을 구하시오.

[수학 구조]
- A=(0,0), B=(d,0) (d=|AB|), 원의 중심 O=(d/2,0), 반지름 r=d/2.
- Q가 AB를 m:n(m>n>0)으로 외분 → AQ:QB = m:n, Q는 B보다 바깥쪽(양의 x축 방향)에 위치.
  외분 공식 Q=(m·B-n·A)/(m-n) 에서 Q_x = m·d/(m-n).
  BQ = Q_x - d = d·n/(m-n) 이므로, d = BQ·(m-n)/n.
- P는 원 위의 점이면서 접선 QP가 반지름 OP와 수직 (OP⊥PQ) → 이 두 조건으로 P 결정.
  (Q는 원 밖의 점이므로 실제로는 접점이 두 개 나오는데, y≠0인 해를 P로 잡는다.)
- 답은 AP·AQ = 벡터 내적.

원문제: m=5, n=1 (5:1 외분), BQ=√3 → d=4√3, Q=(5√3,0) → AP·AQ = 50.

[파라미터로 뽑아낸 것]
- (m, n): 외분 비율 (묶여서 정수 조건을 만족해야 하는 한 쌍) — 바뀌면 Q의 위치/원의 크기 관계가
  바뀌어 답이 달라진다.
- BQ: 길이 스케일 — 답은 BQ^2 에 비례해서 바뀐다 (내적은 길이의 제곱 차원이므로).
"""
import sympy as sp


def value(prm):
    """조건(외분비 m:n, BQ 길이)으로부터 AP·AQ 를 실제로 기하학적으로 풀어 계산한다."""
    m, n, BQ = prm['m'], prm['n'], prm['BQ']
    if m <= n or n <= 0:
        raise ValueError("외분 조건 위반: m>n>0 이어야 Q가 B 바깥쪽에 생긴다.")

    d = BQ * sp.Rational(m - n, n)            # BQ = d*n/(m-n) 로부터 역산한 |AB|
    A = sp.Matrix([0, 0])
    B = sp.Matrix([d, 0])
    O = (A + B) / 2
    r = d / 2
    Q = sp.Matrix([d + BQ, 0])                # Q는 B로부터 BQ 만큼 더 바깥쪽

    x, y = sp.symbols('x y', real=True)
    P = sp.Matrix([x, y])
    eqs = [
        (P - O).dot(P - O) - r ** 2,          # P가 원 위
        (Q - P).dot(P - O),                   # 접선조건: QP ⊥ OP
    ]
    sols = [s for s in sp.solve(eqs, [x, y], dict=True) if sp.simplify(s[y]) != 0]
    if not sols:
        raise ValueError("접점 P가 존재하지 않는 파라미터 조합입니다.")
    sol = sols[0]

    AP = P.subs(sol) - A
    AQ = Q - A
    return sp.simplify(AP.dot(AQ))


CANDIDATE = 50                                 # ★원문제 정답 (절대 변경 금지)
PARAMS = dict(m=5, n=1, BQ=sp.sqrt(3))         # 5:1 외분, BQ=√3


def solve(prm):
    return value(prm)


def statement(prm):
    return (
        f"그림과 같이 선분 AB를 지름으로 하는 원 위의 점 P에서의 접선과 직선 AB가 "
        f"만나는 점을 Q라 하자. 점 Q가 선분 AB를 {prm['m']}:{prm['n']}로 외분하는 점이고, "
        f"BQ={sp.nsimplify(prm['BQ'])}일 때, AP·AQ (벡터 내적)의 값을 구하시오."
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('answer =', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
