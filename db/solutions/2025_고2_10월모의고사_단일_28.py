from sympy import symbols, solve, Rational

a2 = Rational(-4, 3)
f = lambda x: a2 * x + Rational(10, 3) if (x < 1 or x > 1) else 'c'

f0 = Rational(10, 3)
f2 = a2 * 2 + Rational(10, 3)

# 조건 검증
lim_val = a2 + Rational(10, 3)  # 극한값
expected_lim = 3 * f2

check1 = (f0 + f2 == 4)
check2 = (lim_val == expected_lim)
check3 = (f2 != 0)

# x=1에서 f(x)=2가 되므로 [0,1)과 (1,2]에서는 f(x)!=2
for test_x in [0, 0.5, 1.5, 2]:
    if test_x != 1:
        val = a2 * test_x + Rational(10, 3)
        if val == 2:
            print("VERIFY_FAIL")
            exit()

if check1 and check2 and check3:
    answer = f0 / f2
    if answer == 5:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")