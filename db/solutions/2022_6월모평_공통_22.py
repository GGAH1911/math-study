from sympy import symbols, Rational, diff, solve
from math import gcd

CANDIDATE = '61'

x = symbols('x', real=True)

# 함수 정의: f(x) = -1/16 * (x+3)^2 * (x-5)
f = Rational(-1, 16) * (x + 3)**2 * (x - 5)

# f'(x) 계산
f_prime = diff(f, x)

# 조건 (가) 검증: f(x)=0의 서로 다른 실근이 2개
roots_f = solve(f, x)
distinct_roots_f = list(set(roots_f))
cond_ga = len(distinct_roots_f) == 2

# 조건 주어진 값 검증: f(1) = 4
f_at_1 = f.subs(x, 1)
cond_f1_eq_4 = (f_at_1 == 4)

# 조건 주어진 값 검증: f'(1) = 1
f_prime_at_1 = f_prime.subs(x, 1)
cond_fprime1_eq_1 = (f_prime_at_1 == 1)

# 조건 주어진 값 검증: f'(0) > 1
f_prime_at_0 = f_prime.subs(x, 0)
cond_fprime0_gt_1 = (f_prime_at_0 > 1)

# 조건 (나) 검증: f(x-f(x))=0의 서로 다른 실근이 3개
# f(x-f(x))=0 <=> x-f(x)=-3 또는 x-f(x)=5
# 즉, f(x)=x+3 또는 f(x)=x-5

eq1 = f - (x + 3)  # f(x) = x+3
roots_eq1 = solve(eq1, x)

eq2 = f - (x - 5)  # f(x) = x-5
roots_eq2 = solve(eq2, x)

all_roots_combined = roots_eq1 + roots_eq2
unique_roots_combined = list(set(all_roots_combined))
cond_na = len(unique_roots_combined) == 3

# f(0) 계산
f_at_0 = f.subs(x, 0)

# sympy Rational에서 분자(p), 분모(q) 추출
# f(0) = 45/16 이므로 q=45 (분자), p=16 (분모)
q = f_at_0.p  # 분자
p = f_at_0.q  # 분모

# gcd(p, q) = 1 확인 (서로소)
g = gcd(p, q)
cond_coprime = (g == 1)

# p+q 계산
p_plus_q = p + q

# CANDIDATE와 비교
cond_answer = (p_plus_q == int(CANDIDATE))

# 모든 조건 만족 확인
all_satisfied = (cond_ga and cond_f1_eq_4 and cond_fprime1_eq_1 and 
                 cond_fprime0_gt_1 and cond_na and cond_coprime and cond_answer)

if all_satisfied:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")