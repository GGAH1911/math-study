"""2025 고2 6월 단일 18 (지수·로그, 객관식)
E: y=a^(ax), L: y=(1/a)log_a(x-1/a)-1/a.
C = L의 x절편: (1/a)log_a(x-1/a)-1/a=0 → x_C=a+1/a.
D = (C 지나는 기울기-1 직선)∩E: x_D+a^(a x_D)=a+1/a → x_D=1/a, D=(1/a, a).
A: x_A=x_D+1/a=2/a, A=(2/a, a²). B=(A 지나는 -1직선)∩L.
AD 원점통과: a²/(2/a)=a/(1/a) → a³/2=a² → a=2.
a=2: A(1,4) B(9/2,1/2) C(5/2,0) D(1/2,2), 신발끈 넓이=55/8=보기⑤."""
import sympy as sp

CANDIDATE = 5
choices = {1: sp.Rational(35, 8), 2: sp.Integer(5), 3: sp.Rational(45, 8),
           4: sp.Rational(25, 4), 5: sp.Rational(55, 8)}


def solve(origin_k=1):
    a = sp.symbols('a', positive=True)
    # AD 원점통과 조건: a³/2 = origin_k·a²  → a = 2·origin_k
    sols = [s for s in sp.solve(sp.Eq(a**3 / 2, origin_k * a**2), a) if s.is_real and s > 1]
    if not sols:
        return -1
    av = max(sols)
    A = (sp.Integer(2) / av, av**2)              # (2/a, a²)
    D = (1 / av, av)                             # (1/a, a)
    C = (av + 1 / av, sp.Integer(0))             # L의 x절편
    # B = (A 지나는 기울기-1 직선) ∩ L,  x+y = x_A+y_A
    s = A[0] + A[1]
    x = sp.symbols('x', positive=True)
    Lf = sp.log(x - 1 / av, av) / av - 1 / av
    xb = sp.nsolve(Lf - (s - x), x, float(s) / 2)
    B = (xb, s - xb)
    pts = [A, B, C, D]                           # 신발끈 (A→B→C→D)
    area = abs(sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1]
                   for i in range(4))) / 2
    area = sp.nsimplify(area, rational=True)
    for num, cval in choices.items():
        if sp.simplify(area - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
