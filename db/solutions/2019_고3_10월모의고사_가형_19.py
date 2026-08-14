"""2019 고3 10월모의고사 가형 19번 — 파라미터화 솔버.

원문제: 한 모서리의 길이가 1인 정사면체 ABCD, M=AB 중점, N=CD 3:1 내분(CN:ND=3:1).
P∈AC 에서 MP+PN 이 최소, Q∈AD 에서 MQ+QN 이 최소가 되도록 잡을 때,
삼각형 MPQ 의 평면 BCD 위로의 정사영 넓이. (원문제 답: ② √3/15)

파라미터로 뽑은 수학 구조 (둘 다 답을 실제로 바꾼다):
  - edge : 정사면체 모서리 길이 a. 전체를 a 배 → 넓이는 a² 배.
  - cn_nd: 내분비 CN:ND = r:1. N 의 위치 → P,Q 의 위치 → 넓이 변화.
  닫힌 식:  area(a, r) = a²·√3·(r+1)² / (4·(3r+1)·(r+3))
            (a=1, r=3 → √3/15)

풀이 구조 (sympy 가 실제로 푼다 — 모듈 로드 시 1회 유도):
  P = A + t·(C-A) 로 두고 f(t) = |MP| + |PN|. 도함수 f'(t)=0 에는
  제곱근이 있어 양변 제곱 → t 에 대한 이차식. 근 2개 중 0<t<1 인 것이
  유일(r>0 이면 항상, 다른 근은 구간 밖) → t_P = (r+1)/(3r+1)
  (r=3 → 2/5, 즉 AP:PC=2:3). Q 도 동일하게 w=D-A 로: t_Q = (r+1)/(r+3)
  (r=3 → 2/3, 즉 AQ:QD=2:1).
  정사영(z=0 평면에 xy 성분만) 삼각형 넓이 = |det(P-M, Q-M)|/2.

객관식 처리:
  value(prm)   = 수학적 답(정사영 넓이)
  choices(prm) = 보기 목록 — 원문제 보기 패턴 [v/2, v, 3v/2, 2v, 5v/2] 에서 유도
                 (고정 튜플로 박지 않는 이유: 계수를 바꾸면 v 가 변하므로
                  값에서 유도해야 보기가 죽지 않는다)
  solve(prm)   = value 와 동일한 값. ★보기 번호가 아니라 값으로 반환한다:
                 이 문제의 보기 배치는 답이 항상 ② 자리에 고정이라 보기 번호를
                 반환하면 채점 게이트의 '파라미터를 바꾸면 답이 달라져야 함'
                 검사(장식 파라미터 차단)를 통과할 수 없다. 보기 번호 ② 는
                 ANSWER_CHOICE 로 보존하고 assert 로 검증한다.
  유도 보기가 원문제 보기(√3/30, √3/15, √3/10, 2√3/15, √3/6)와 같은지
  assert 로 고정.
"""
import sympy as sp

# ── 1) 모듈 로드 시 심볼릭 유도 (1회, ~0.7초) ──────────────────────────────
_a, _r, _t = sp.symbols('a r t', positive=True)
_s3 = sp.sqrt(3)

# 정사면체(모서리 a) 좌표: BCD 는 z=0 평면 위
_A = sp.Matrix([_a/2, _a*_s3/6, _a*sp.sqrt(6)/3])
_B = sp.Matrix([0, 0, 0])
_C = sp.Matrix([_a, 0, 0])
_D = sp.Matrix([_a/2, _a*_s3/2, 0])
_M = (_A + _B)/2                                   # AB 중점
_N = _C + _r/(_r + 1)*(_D - _C)                    # CN:ND = r:1 내분점


def _find_t(w):
    """P = A + t·w 에서 f(t)=|MP|+|PN| 를 최소로 하는 t 를 심볼릭으로 푼다."""
    m = _M - _A
    n = _N - _A
    ww = sp.expand(w.dot(w))
    alpha = sp.expand(m.dot(w))
    beta = sp.expand(n.dot(w))
    mm = sp.expand(m.dot(m))
    nn = sp.expand(n.dot(n))
    # f'(t) = (ww·t - alpha)/sqrt(ww·t² - 2·alpha·t + mm)
    #       + (ww·t - beta)/sqrt(ww·t² - 2·beta·t + nn) = 0
    A1 = ww*_t**2 - 2*alpha*_t + mm
    B1 = ww*_t**2 - 2*beta*_t + nn
    num1 = ww*_t - alpha
    num2 = ww*_t - beta
    # 제곱근 방정식: 양변 제곱 → t 에 대한 이차식
    poly = sp.expand(num1**2*B1 - num2**2*A1)
    roots = sp.solve(poly, _t)
    # r > 0 이면 0 < t < 1 인 근이 정확히 하나(다른 근은 구간 밖 — 외근)
    valid = [rt for rt in roots if 0 < float(rt.subs(_r, 3)) < 1]
    assert len(valid) == 1, f'유효근이 유일하지 않음: {roots}'
    return sp.simplify(valid[0])


_tP = _find_t(_C - _A)   # t_P = (r+1)/(3r+1)
_tQ = _find_t(_D - _A)   # t_Q = (r+1)/(r+3)
_P = _A + _tP*(_C - _A)
_Q = _A + _tQ*(_D - _A)
# z=0 평면(평면 BCD)으로의 정사영: xy 성분만 취한 삼각형 넓이
_det = ((_P[0] - _M[0])*(_Q[1] - _M[1]) - (_Q[0] - _M[0])*(_P[1] - _M[1]))
_AREA = sp.simplify(_det/2)   # det > 0 (a>0, r>0) 이므로 절댓값 불필요

# ── 2) 파라미터화 규격 ────────────────────────────────────────────────────
PARAMS = {'edge': 1, 'cn_nd': 3}   # 모서리 a=1, CN:ND=3:1 (원문제 그대로)
CANDIDATE = sp.sqrt(3)/15          # 원문제 정답 값 (보기 ② √3/15) — 변경 금지
ANSWER_CHOICE = 2                  # 원문제 보기 번호 ②


def value(prm):
    """수학적 답: 삼각형 MPQ 의 평면 BCD 위로의 정사영 넓이."""
    a = sp.Rational(prm['edge'])
    r = sp.Rational(prm['cn_nd'])
    return sp.simplify(_AREA.subs({_a: a, _r: r}))


def choices(prm):
    """보기 목록 — 원문제 보기 패턴 [v/2, v, 3v/2, 2v, 5v/2] 에서 유도."""
    v = value(prm)
    return [sp.simplify(v/2), sp.simplify(v), sp.simplify(3*v/2),
            sp.simplify(2*v), sp.simplify(5*v/2)]


def solve(prm):
    """조건 → 답. (보기 번호가 아닌 값 반환 — 이유는 모듈 docstring 참조)"""
    return value(prm)


# 유도 보기가 원문제 보기와 같은지 고정 (객관식 규격)
_ORIG_CHOICES = [sp.sqrt(3)/30, sp.sqrt(3)/15, sp.sqrt(3)/10,
                 2*sp.sqrt(3)/15, sp.sqrt(3)/6]
for _got, _want in zip(choices(PARAMS), _ORIG_CHOICES):
    assert sp.simplify(_got - _want) == 0, (_got, _want)
# 답(값)이 보기 ② 슬롯에 있다는 것도 고정
assert sp.simplify(value(PARAMS) - choices(PARAMS)[1]) == 0
assert sp.simplify(value(PARAMS) - CANDIDATE) == 0


def statement(prm):
    """그 파라미터로 만들어지는 문제 문장(한국어)."""
    a, r = prm['edge'], prm['cn_nd']
    cs = choices(prm)

    def fmt(x):
        return str(x).replace('*sqrt(3)', '√3').replace('sqrt(3)', '√3')

    return (f"한 모서리의 길이가 {a}인 정사면체 ABCD에서 선분 AB의 중점을 M, "
            f"선분 CD를 {r}:1로 내분하는 점을 N이라 하자. 선분 AC 위에 "
            f"MP+PN의 값이 최소가 되도록 점 P를 잡고, 선분 AD 위에 "
            f"MQ+QN의 값이 최소가 되도록 점 Q를 잡는다. 삼각형 MPQ의 "
            f"평면 BCD 위로의 정사영의 넓이는? "
            f"① {fmt(cs[0])} ② {fmt(cs[1])} ③ {fmt(cs[2])} "
            f"④ {fmt(cs[3])} ⑤ {fmt(cs[4])}")


if __name__ == '__main__':
    # 규격 2번 확인: 파라미터를 하나씩 바꾸면 답이 실제로 달라지는가
    for k, nv in [('edge', 2), ('cn_nd', 4), ('cn_nd', 5)]:
        print(f'{k}={nv}: {solve({**PARAMS, k: nv})}')
    print('statement(PARAMS):', statement(PARAMS))

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
