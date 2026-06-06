"""2026 9월모평 미적분 28 (도함수의_활용_심화, 객관식)
f(x)=g(x)-tan g(x). f'(x)=-g'(x)tan²g(x).
(나) sin g(π)=0 → g(π)=nπ, tan g(π)=0 → f'(π)=0. (가) f''(π)=0 → f는 x=π에서 변곡+수평접선
→ f(x)=c(x-π)³+f(π), f(π)=g(π)=nπ. 극한 g→3π/2(위에서) → n=2.
(가) f(0)=0 → c(-π)³+nπ=0 → c=n/π². f'(0)=3cπ²=3n.
f(0)=0 → tan g(0)=g(0) → f'(0)=-g'(0)g(0)² → g'(0)g(0)²=-3n=-6=보기②."""
import sympy as sp

CANDIDATE = 2
choices = {1: -12, 2: -6, 3: -1, 4: 3, 5: 9}


def solve(n=2, f0=0):
    pi = sp.pi
    # g(π)=nπ → f(π)=nπ; f(x)=c(x-π)³+nπ; f(0)=f0 → c=(nπ-f0)/π³
    c = (n * pi - f0) / pi ** 3
    f_prime_0 = 3 * c * pi ** 2                  # f'(0)=3c(0-π)²
    val = sp.simplify(-f_prime_0)                # g'(0)·g(0)² = -f'(0)
    for num, cval in choices.items():
        if sp.simplify(val - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
