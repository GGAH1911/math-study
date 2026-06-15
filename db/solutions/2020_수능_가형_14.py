from sympy import Rational, simplify

# 원래 조건: 공 개수 10(번호1), 20(번호2), 30(번호3), 총 60
counts = {1: 10, 2: 20, 3: 30}
N = sum(counts.values())
prob = {x: Rational(c, N) for x, c in counts.items()}

# 확률변수 X 의 분포로부터 직접 계산
EX = sum(x * prob[x] for x in counts)
EX2 = sum(x**2 * prob[x] for x in counts)
VX = simplify(EX2 - EX**2)

# 문제에서 주어진 값과 일치하는지 확인
assert EX == Rational(7, 3), 'E(X) mismatch'

n = 10  # 표본 크기
VXbar = simplify(VX / n)               # (나) q = V(Xbar)
EY = simplify(n * EX)                   # E(Y) = 70/3 확인
VY = simplify(n**2 * VXbar)             # (다) r = V(Y)

assert EY == Rational(70, 3), 'E(Y) mismatch'

p = VX        # (가)
q = VXbar     # (나)
r = VY        # (다)
total = simplify(p + q + r)

CANDIDATE = Rational(37, 6)
print('p+q+r =', total)
if simplify(total - CANDIDATE) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
