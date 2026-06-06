from sympy import symbols, Rational

# 등비수열의 첫째항과 공비
a = Rational(1, 3)
r = 3

# S_n 계산 함수
def S(n):
    return a * (r**n - 1) / (r - 1)

# 주어진 조건 검증: S_{n+3} - S_n = 13 × 3^(n-1)
test_passed = True
for n in range(1, 6):
    lhs = S(n + 3) - S(n)
    rhs = 13 * (3**(n - 1))
    if lhs != rhs:
        test_passed = False
        print(f"VERIFY_FAIL at n={n}: {lhs} != {rhs}")
        break

if test_passed:
    # a_4 계산
    a4 = a * (r**3)
    if a4 == 9:
        print("VERIFY_PASS")
    else:
        print(f"VERIFY_FAIL: a_4 = {a4}, expected 9")
else:
    print("VERIFY_FAIL")