from sympy import Rational

def converges_exact(r):
    # a_n = r**n/(8**n+9**n) = (r/9)**n / (1+(8/9)**n); 둘째 인수 -> 1
    # => 등비수열 (r/9)**n 의 수렴과 동치, 즉 -1 < r/9 <= 1
    t = Rational(r, 9)
    return (t > -1) and (t <= 1)

def converges_num(r):
    t = r / 9.0
    val = 1.0
    tail = []
    for k in range(1, 3001):
        val *= t
        a = val / (1.0 + (8.0/9.0)**k)
        if abs(a) > 1e8:
            return False
        if k > 2950:
            tail.append(a)
    return (max(tail) - min(tail)) < 1e-6

ints = []
for x in range(-200, 201):
    r = 4*x - 1
    ce = converges_exact(r)
    cn = converges_num(r)
    assert ce == cn, (x, r, ce, cn)
    if ce:
        ints.append(x)

count = len(ints)
print('integers:', ints, 'count:', count)
if count == 4 and ints == [-1, 0, 1, 2]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
