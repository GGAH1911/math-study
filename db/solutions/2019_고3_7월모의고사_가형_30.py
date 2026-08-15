"""2019 고3 7월모의고사 가형 30번 — 파라미터화 솔버.

[문제의 수학 구조]
사차함수 f(x)=k x^2 (x-s)^2  (k>0, s>0인 짝수, 극대점 a=s/2>0)
g(x) = (1-cos(πx))/f(x)  (f(x)≠0),  = C·π²  (f(x)=0)

g가 실수 전체에서 미분가능하려면 f의 두 근(0, s)에서 극한이 상수 C·π²와 일치해야 하고,
1-cos(πx)의 국소 전개(x=r+t, r이 짝수정수 근일 때 1-cosπx ≈ (π²/2)t²)로부터
  k·s^2 = 1/(2C)                       … (근 0, s 공통 조건)
가 나온다. 또 g(m)=G_num/G_den (m은 홀수, 1-cos(πm)=2) 이 주어지면
  k·m^2·(m-s)^2 = 2·G_den/G_num
이 추가되어 (k, s)가 정해진다. 이때 s는 "짝수인 양의 정수"라는 조건(근이 짝수정수여야
1-cosπx가 함께 0이 됨)으로 유일해를 고른다. 마지막으로 g(n) = 2/f(n) = q/p (n도 홀수)을
구해 p+q가 답이 된다.

★파라미터화 지점: m(값이 주어지는 점), n(값을 구할 점), C_num/C_den(f=0일 때 상수의
π² 계수), G_num/G_den(g(m)의 값) — 이 넷이 f의 계수 k와 두 번째 근 s를 통째로 결정한다.
단, (k,s)가 "s는 양의 짝수정수"를 만족해야 문제가 성립하므로, C·G 조합을 아무렇게나
바꾸면 해가 없거나 여럿이 되어 예외가 난다. 그래서 (k,s,m,n)을 먼저 정하고 그로부터
C,G를 역산해 만든 자연스러운 조합들을 VARIANTS 로 제시한다(공통_해 구조).
"""
import sympy as sp

CANDIDATE = 95  # ★원문제 정답, 절대 변경 금지

# 원문제: m=1(g(1)=2/7 이 주어짐), n=-1(g(-1) 을 구함), f=0일 때 상수 = (7/128)π²
PARAMS = dict(m=1, n=-1, C_num=7, C_den=128, G_num=2, G_den=7)

# (k,s,m,n)을 먼저 골라 C,G를 역산해서 만든, 실제로 성립하는 다른 조합들.
# (원문제와 다른 답을 내야 하므로 base(=95)와 다른 것들만 담는다)
VARIANTS = [
    dict(m=1, n=-1, C_num=3, C_den=32, G_num=2, G_den=3),   # k=1/3, s=4  -> 31
    dict(m=1, n=-3, C_num=5, C_den=144, G_num=1, G_den=5),  # k=2/5, s=6  -> 734
    dict(m=3, n=-1, C_num=1, C_den=16, G_num=4, G_den=9),   # k=1/2, s=4  -> 29
]


def solve(prm):
    m, n = prm['m'], prm['n']
    C_num, C_den = prm['C_num'], prm['C_den']
    G_num, G_den = prm['G_num'], prm['G_den']

    if m % 2 == 0 or n % 2 == 0:
        # 1-cos(πx)=2 가 되려면 x는 홀수여야 함 (짝수면 f=0 분기와 겹쳐 정보가 안 됨)
        raise ValueError('m, n 은 홀수여야 한다')
    if m == 0 or n == 0:
        raise ValueError('m, n 은 0이 아니어야 한다')

    k, s = sp.symbols('k s', positive=True)
    # 근 0, s에서 g가 미분가능하려면 극한값이 C_num/C_den * π² 이어야 함
    eq1 = sp.Eq(k * s**2, sp.Rational(C_den, 2 * C_num))
    # g(m) = G_num/G_den 로부터 f(m) 결정
    eq2 = sp.Eq(k * m**2 * (m - s)**2, sp.Rational(2 * G_den, G_num))

    sols = sp.solve([eq1, eq2], [k, s], dict=True)

    # f의 두 근(0, s)이 모두 짝수인 양의 정수여야 g가 미분가능(1-cosπx도 함께 0)하므로
    # 그 조건을 만족하는 해만 유효하다.
    valid = [t for t in sols
             if t[s].is_integer and t[s] % 2 == 0 and t[s] > 0
             and t[k] > 0 and t[s] != m]
    if len(valid) != 1:
        raise ValueError(f'조건을 만족하는 (k,s)가 유일하지 않다: {valid}')

    kv, sv = valid[0][k], valid[0][s]
    f_n = kv * n**2 * (n - sv)**2
    if f_n == 0:
        raise ValueError('f(n)=0 이 되어 g(n)이 정의되지 않는다')

    g_n = sp.nsimplify(sp.Rational(2) / f_n)
    q, p = sp.fraction(g_n)   # g(n) = q/p
    if sp.gcd(p, q) != 1:
        raise ValueError('p, q 가 서로소가 아니다 (문제 조건 위반)')
    return int(p + q)


def statement(prm):
    m, n = prm['m'], prm['n']
    C_num, C_den = prm['C_num'], prm['C_den']
    G_num, G_den = prm['G_num'], prm['G_den']
    Cf = sp.Rational(C_num, C_den)
    Gf = sp.Rational(G_num, G_den)
    return (
        "x=a(a>0)에서 극댓값을 갖는 사차함수 f(x)에 대하여\n"
        "함수 g(x)가\n"
        "g(x) = (1-cos(πx))/f(x)  (f(x) ≠ 0),\n"
        f"     = ({Cf.p}/{Cf.q})π^2  (f(x) = 0)\n"
        "일 때, 함수 g(x)는 실수 전체의 집합에서 미분가능하고 다음 조건을 만족시킨다.\n"
        "(가) g'(0) × g'(2a) ≠ 0\n"
        "(나) 함수 g(x)는 x=a에서 극값을 갖는다.\n\n"
        f"g({m})={Gf.p}/{Gf.q} 일 때, g({n})=q/p 이다. p+q의 값을 구하시오. "
        "(단, p와 q는 서로소인 자연수이다.)"
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
