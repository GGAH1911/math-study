import sympy as sp
from sympy import sqrt, simplify, Rational, Integer

def f(x):
    return -x**2 - 2*x + 1

def g(x):
    return x**2 - 2*x - 1

# ㄱ: a=0이면 f가 (-inf,0)에서 단사가 아님 → (0,k) not in A
x1, x2 = Rational(-1,2), Rational(-3,2)
gar_ok = (f(x1) == f(x2)) and (x1 != x2)  # f not injective on (-inf,0)

# ㄴ: (-1,4) in A 검증
a_n, b_n = Integer(-1), Integer(4)
cond1 = (a_n <= -1)
cond2 = (1 - b_n <= a_n)  # -3 <= -1
cond3 = (f(a_n) == g(a_n + b_n))  # f(-1)=2, g(3)=2
nau_ok = cond1 and cond2 and cond3

# ㄷ: 정수 m in {-3,-2,-1}에 대해 b = (1-m)+sqrt((1-m)(m+3)), sum(m+b) = 5+sqrt(3)
a_vals = [Integer(-3), Integer(-2), Integer(-1)]
total = Integer(0)
for a_val in a_vals:
    b_val = (1 - a_val) + sqrt((1 - a_val) * (a_val + 3))
    # 조건 검증
    assert a_val <= -1
    assert simplify(Integer(1) - b_val - a_val) <= 0, f'cond2 fail for a={a_val}'
    diff = simplify(f(a_val) - g(a_val + b_val))
    assert diff == 0, f'f(a)!=g(a+b) for a={a_val}'
    total += a_val + b_val

da_ok = simplify(total - (5 + sqrt(3))) == 0

if gar_ok and nau_ok and da_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'gar_ok={gar_ok}, nau_ok={nau_ok}, da_ok={da_ok}')
    print(f'total={total}, expected={5+sqrt(3)}')
