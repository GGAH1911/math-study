"""2019 고3 4월모의고사 가형 27번 — 파라미터화 솔버.

문제: 실수 전체에서 미분가능한 f, g 가 있고 g 는 f 의 역함수, g(A)=x_lo, g(B)=x_hi 일 때
      \\int_{x_lo}^{x_hi} C / ( g'(f(x)) {f(x)}^2 ) dx 의 값.

수학 구조:
  g = f^{-1} → g(u)=x ⇔ f(x)=u → 역함수 미분법으로 g'(f(x)) = 1/f'(x).
  피적분함수 = C·f'(x)/f(x)^2 이고 이는 정확히 d/dx[-C/f(x)] 이므로
  ∫_{x_lo}^{x_hi} = C(1/f(x_lo) - 1/f(x_hi)) = C(1/A - 1/B).
  이 값은 f 가 무엇이든 두 경계값 f(x_lo)=A, f(x_hi)=B 에만 의존한다(경로 무관, 대입적분).
  그 사실을 실제로 검증하기 위해, 코드에서는 두 점 (x_lo,A),(x_hi,B) 를 지나는
  구체적인 선형함수 f 를 sympy 로 만들고, g'(f(x))=1/f'(x) 를 대입해 실제로 정적분한다
  (닫힌식을 바로 반환하지 않고 sympy.integrate 로 실행).

파라미터:
  A, B   : g(A)=x_lo, g(B)=x_hi 로 주어지는 f 의 두 함숫값 (⇔ f(x_lo)=A, f(x_hi)=B)
  C      : 피적분함수 분자의 상수배
  x_lo, x_hi : 적분구간 겸 g 의 함숫값(문제 문장 구성에 쓰이고, f 를 구체화하는 데도 쓰인다)
  → A, B, C 를 바꾸면 답이 실제로 달라진다(아래에서 직접 확인).
"""
import sympy as sp


def solve(prm):
    A = sp.Rational(prm['A'])
    B = sp.Rational(prm['B'])
    C = sp.Rational(prm['C'])
    x_lo = sp.Rational(prm['x_lo'])
    x_hi = sp.Rational(prm['x_hi'])
    if x_lo == x_hi:
        raise ValueError('x_lo, x_hi 가 같으면 적분구간이 존재하지 않는다')
    if A == B:
        raise ValueError('f(x_lo)=f(x_hi) 이면 f가 상수라 역함수 g가 존재하지 않는다')

    x = sp.symbols('x')
    slope = (B - A) / (x_hi - x_lo)      # (x_lo,A),(x_hi,B) 를 지나는 선형함수 f 를 구체화
    f = A + slope * (x - x_lo)
    g_prime_at_f = 1 / slope             # f 가 선형이므로 g'(u) 는 상수 = 1/f'(x) = 1/slope
    integrand = C / (g_prime_at_f * f ** 2)
    result = sp.integrate(integrand, (x, x_lo, x_hi))
    return sp.nsimplify(result)


def statement(prm):
    A, B = prm['A'], prm['B']
    C = prm['C']
    x_lo, x_hi = prm['x_lo'], prm['x_hi']
    return (
        "실수 전체의 집합에서 미분가능한 두 함수 f(x), g(x)가 있다.\n"
        f"g(x)가 f(x)의 역함수이고 g({A})={x_lo}, g({B})={x_hi}일 때,\n"
        f"\\int_{{{x_lo}}}^{{{x_hi}}} \\frac{{{C}}}{{g'(f(x))\\{{f(x)\\}}^2}} dx의 값을 구하시오."
    )


# g(2)=1 → f(1)=2, g(5)=5 → f(5)=5, 상수 40, 적분구간 [1,5] (원문제 그대로)
PARAMS = dict(A=2, B=5, C=40, x_lo=1, x_hi=5)
CANDIDATE = 12

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
