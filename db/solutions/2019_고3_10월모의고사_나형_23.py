from sympy import symbols, log, simplify, nsimplify, Rational

CANDIDATE = 4

# 문제의 수학 구조:
#   1이 아닌 두 양수 a, b 가 log_a(b) = k 를 만족.
#   log(b/a) * log_a(N) 의 값을 구하라. (log 는 상용로그, N = 10^m)
#
# 유도:
#   log_a(b) = k  =>  b = a^k
#   log(b/a) = log(a^(k-1)) = (k-1)*log(a)
#   log_a(N) = log_a(10^m) = m / log_a(10) ... 상용로그로는 log_a(10^m) = m*log(10)/log(a)
#   곱: (k-1)*log(a) * m*log(10)/log(a) = m*(k-1)*log(10) = m*(k-1)   (상용로그 log(10)=1)
#
# 원문제는 k=3 (log_a b = 3), N=100 즉 m=2 인 경우이며 답은 m*(k-1) = 2*2 = 4.
#
# 답을 실제로 바꾸는 파라미터: k (log_a b = k), m (N = 10^m, 즉 log_a N)
PARAMS = dict(k=3, m=2)


def solve(prm):
    k = prm['k']
    m = prm['m']

    if k == 1:
        raise ValueError("log_a(b) = 1 이면 b = a 가 되어 문제 조건(전개 자체)이 성립하지 않는다.")

    a = symbols('a', positive=True)
    b = a**k  # log_a(b) = k 로부터

    # log(b/a) : 상용로그 (밑 10)
    log_b_over_a = simplify(log(b / a, 10))

    # log_a(N), N = 10**m : a를 밑으로 하는 로그
    log_a_N = simplify(log(10**m, a))

    expr = simplify(log_b_over_a * log_a_N)

    # a 값에 관계없이 상수여야 함(문제 구조상). 서로 다른 두 a로 검증 후 값 반환.
    v1 = simplify(expr.subs(a, 2))
    v2 = simplify(expr.subs(a, 5))
    if simplify(v1 - v2) != 0:
        raise ValueError("a에 무관한 상수로 정리되지 않음: 문제 조건이 성립하지 않는다.")

    val = nsimplify(v1)
    if val.free_symbols:
        raise ValueError("결과가 수치로 정리되지 않음.")

    return val


def statement(prm):
    k = prm['k']
    m = prm['m']
    N = 10**m
    return (
        f"1이 아닌 두 양수 a, b가 log_a(b)={k}를 만족시킬 때, "
        f"log(b/a) × log_a({N})의 값을 구하시오."
    )


assert solve(dict(k=3, m=2)) == CANDIDATE

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
