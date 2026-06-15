from sympy import Rational, binomial

R0, B0, Y0 = 6, 3, 3
TOT = R0 + B0 + Y0

def scores(x, y, z):
    sa = 3*x + 2*y + 2*z
    sb = 1*x + 6*y + 2*z
    sc = 1*x + 2*y + 6*z
    return sa, sb, sc

def comp_prob(x, y, z):
    n = x + y + z
    return Rational(binomial(R0, x) * binomial(B0, y) * binomial(Y0, z), binomial(TOT, n))

# (가): cases (6,1,2),(6,2,1) -> A score exactly 24, any order, stops at 9th draw
p_i = comp_prob(6, 1, 2)
p_ii = comp_prob(6, 2, 1)
assert p_i == p_ii
p = p_i

# (나): case (6,2,2) -> A=26>24 so 10th ball must be red; first9=(5,2,2), remaining 1R1B1Y
q = comp_prob(5, 2, 2) * Rational(1, 3)

# Independent brute force over all draw orders (no replacement), first-crossing stop
def brute_A_only():
    total = [Rational(0)]
    def dfs(r, b, y, prob):
        sa, sb, sc = scores(R0 - r, B0 - b, Y0 - y)
        if max(sa, sb, sc) >= 24:
            if sa >= 24 and sb < 24 and sc < 24:
                total[0] += prob
            return
        n = r + b + y
        if n == 0:
            return
        if r: dfs(r-1, b, y, prob * Rational(r, n))
        if b: dfs(r, b-1, y, prob * Rational(b, n))
        if y: dfs(r, b, y-1, prob * Rational(y, n))
    dfs(R0, B0, Y0, Rational(1))
    return total[0]

full = brute_A_only()
CANDIDATE = Rational(27, 220)

ok = (full == 2*p + q and full == Rational(9, 55) and
      p == Rational(9, 220) and q == Rational(9, 110) and
      (p + q) == CANDIDATE)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
