import sympy as sp
from sympy import sqrt, simplify

CANDIDATE = 38

# 파라미터 정의
a = -3
c = -2*a/9  # = 2/3
b = sp.Symbol('b', real=True)

# 함수 정의
def f(x):
    return a*(x+1)**2 + b

def g(x):
    return c*x**3 + 2*a*x + (a+b)

def f_prime(x):
    return 2*a*(x+1)

def g_prime(x):
    return 3*c*x**2 + 2*a

# 조건 (가) 검증: h(x) = h(0)의 근들
# x <= 0: f(x) = a+b => (x+1)^2 = 1 => x = -2, 0
# x > 0: g(x) = a+b => x(cx^2 + 2a) = 0 => x = sqrt(-2a/c) = 3
roots = [-2, 0, 3]
sum_roots = sum(roots)
assert sum_roots == 1, f"조건 (가) 실패: {sum_roots}"

# 조건 (나) 검증
# 극값: x=-1에서 극대, x=sqrt(3)에서 극소
# 최댓값: f(-1) = b
# 최솟값: g(sqrt(3)) = 2*sqrt(3) - 6*sqrt(3) + (b-3) = -4*sqrt(3) + b - 3
max_val = f(-1)
min_val = g(sqrt(3))
difference = simplify(max_val - min_val)
expected_diff = 3 + 4*sqrt(3)
assert simplify(difference - expected_diff) == 0, f"조건 (나) 실패: {difference}"

# h'(-3) + h'(4) 계산
h_prime_neg3 = f_prime(-3)  # x <= 0이므로 f'(-3) 사용
h_prime_4 = g_prime(4)      # x > 0이므로 g'(4) 사용
result = h_prime_neg3 + h_prime_4

assert result == CANDIDATE, f"계산 오류: {result} != {CANDIDATE}"
print('VERIFY_PASS')