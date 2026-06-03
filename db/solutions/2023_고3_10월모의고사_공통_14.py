from sympy import Rational

b_lower = Rational(-19, 3)
b_upper = Rational(-7, 3)

def F(n, b):
    return (n - 4) * (n**2 - 2*n + 4 + 3*b) / 3

# 1) 주어진 조건 검증: 모든 자연수 n에서 F(n) >= 0
constraint_ok = True
for b_val in [b_lower, b_upper, Rational(-3, 1)]:
    for n_val in range(1, 20):
        if F(n_val, b_val) < 0:
            # b=-3은 범위 내 임의값
            pass
# 범위 양 끝점에서만 체크
for b_val in [b_lower, b_upper]:
    for n_val in range(1, 20):
        val = F(n_val, b_val)
        if val < 0:
            constraint_ok = False

# 2) ㄱ: f(2) = b < 0 (b_upper = -7/3 < 0)
gak = b_upper < 0

# 3) ㄴ: F(3) > F(2)? => F(3)-F(2) = (1+3b)/3 < 0 for all valid b => FALSE
nak_diff_upper = (1 + 3*b_upper) / 3  # should be < 0
nak_diff_lower = (1 + 3*b_lower) / 3
nak_false = (nak_diff_upper < 0) and (nak_diff_lower < 0)

# 4) ㄷ: 6 <= F(6) <= 14
F6_at_lower = F(6, b_lower)  # expect 6
F6_at_upper = F(6, b_upper)  # expect 14
dat = (F6_at_lower == 6) and (F6_at_upper == 14)

if constraint_ok and gak and nak_false and dat:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'constraint_ok={constraint_ok}, gak={gak}, nak_false={nak_false}, dat={dat}')
    print(f'F6_lower={F6_at_lower}, F6_upper={F6_at_upper}')
