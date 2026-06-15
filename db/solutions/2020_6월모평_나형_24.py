from sympy import symbols, solve

# 2020 6월모평 나형 24: 공비 양수 등비수열, a1=2, a5/a3=9. sum_{k=1}^4 a_k?
CANDIDATE = 80
r = symbols('r', positive=True)
a1 = 2
# a5/a3 = (a1 r^4)/(a1 r^2) = r^2 = 9, 공비 양수
rr = [s for s in solve(r**2 - 9, r) if s > 0][0]   # r = 3
total = sum(a1 * rr**(k - 1) for k in range(1, 5))  # a1..a4
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL')
