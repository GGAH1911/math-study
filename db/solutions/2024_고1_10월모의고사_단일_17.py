from sympy import Rational, sqrt

a = Rational(13, 2)

def f(x):
    return (x - a)**2 + 1

# 조건(가) 검증: 정수 p, q (p≠q) with f(p)=f(q)
p, q = 6, 7
assert p != q and f(p) == f(q), 'VERIFY_FAIL: 조건(가) 실패'

# 조건(나) 검증: max*min != f(n)*f(n+3)인 자연수 n의 집합이 {4,5,6}
failing_ns = []
for n in range(1, 20):
    lo, hi = n, n+3
    # 꼭짓점이 구간 내부에 있으면 min=1, 아니면 min=min(f(n),f(n+3))
    if lo < a < hi:
        mn = 1
    else:
        mn = min(f(lo), f(hi))
    mx = max(f(lo), f(hi))
    product_maxmin = mx * mn
    product_endpoints = f(lo) * f(hi)
    if product_maxmin != product_endpoints:
        failing_ns.append(n)

assert failing_ns == [4, 5, 6], f'VERIFY_FAIL: failing_ns={failing_ns}'

# f(8) 검증
result = f(8)
assert result == Rational(13, 4), f'VERIFY_FAIL: f(8)={result}'

print('VERIFY_PASS')
