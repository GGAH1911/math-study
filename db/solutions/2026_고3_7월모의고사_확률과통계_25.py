# 1..7 중 2장. 차가 2의 배수 = 두 수의 홀짝이 같음.
import sympy as sp
from itertools import combinations

cards = range(1, 8)
tot = list(combinations(cards, 2))
good = [p for p in tot if (p[1] - p[0]) % 2 == 0]
val = sp.Rational(len(good), len(tot))
assert len(tot) == sp.binomial(7, 2)
choices = {1: sp.Rational(3, 7), 2: sp.Rational(10, 21), 3: sp.Rational(11, 21),
           4: sp.Rational(4, 7), 5: sp.Rational(13, 21)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [1] else 'VERIFY_FAIL')
