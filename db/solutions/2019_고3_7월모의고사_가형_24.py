"""2019 고3 7월모의고사 가형 24번 — 파라미터화 솔버.

문제 구조: 이항분포 X~B(n,p) 에서 선형변환 Y=aX+b 의 기댓값이 주어질 때
V(Y)=a^2*n*p*(1-p) 를 구한다.

파라미터로 뽑은 수학적 자유도:
  n      : 시행 횟수 (이항분포 B(n,p)의 n)
  a, b   : 선형변환 Y = aX + b 의 계수
  E_lin  : E(Y) = E(aX+b) 의 주어진 값  → 이 조건으로 p 를 역산한다

p = (E_lin - b) / (a*n) 로 sympy 방정식을 세워 실제로 풀고,
0<p<1 을 만족하지 않으면(=이항분포로 성립 불가) 예외를 던진다.
"""
import sympy as sp

CANDIDATE = 64  # ★원문제 정답 — 절대 바꾸지 않는다

PARAMS = dict(n=72, a=2, b=-3, E_lin=45)


def solve(prm):
    n, a, b, E_lin = prm['n'], prm['a'], prm['b'], prm['E_lin']
    p = sp.symbols('p')
    # E(aX+b) = a*n*p + b = E_lin  (X~B(n,p) 이므로 E(X)=n*p)
    eq = sp.Eq(a * n * p + b, E_lin)
    sols = sp.solve(eq, p)
    if not sols:
        raise ValueError('p 에 대한 해가 없다')
    p_val = sp.nsimplify(sols[0])
    if not (p_val.is_number and 0 < p_val < 1):
        raise ValueError(f'p={p_val} 가 (0,1) 범위를 벗어나 이항분포로 성립하지 않는다')
    var_y = a**2 * n * p_val * (1 - p_val)  # V(aX+b) = a^2 * V(X) = a^2 * n*p*(1-p)
    return sp.nsimplify(var_y)


def statement(prm):
    n, a, b, E_lin = prm['n'], prm['a'], prm['b'], prm['E_lin']
    return (
        f'이항분포 B({n}, p)를 따르는 확률변수 X에 대하여 '
        f'E({a}X{"+" if b >= 0 else ""}{b})={E_lin}일 때, '
        f'V({a}X{"+" if b >= 0 else ""}{b})의 값을 구하시오.'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
