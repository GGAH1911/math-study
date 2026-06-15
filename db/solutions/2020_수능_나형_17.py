from sympy import divisor_count, divisors, log, Rational, simplify, symbols, nsimplify
from sympy import Integer

# 36의 모든 양의 약수
n = 36
divs = divisors(n)
assert len(divs) == 9, divs

# sum over divisors of (-1)^{f(a)} * log(a)
expr = 0
for a in divs:
    fa = divisor_count(a)           # 양의 약수의 개수
    sign = (-1)**fa
    expr += sign * log(Integer(a))
expr = simplify(expr)

# 기대값: log2 + log3 (= log6)
expected = log(Integer(2)) + log(Integer(3))
if simplify(expr - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', expr)
