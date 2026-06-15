from sympy import symbols, expand, simplify

n = symbols('n', positive=True, integer=True)

# S_n = n^3 + n
S_n = n**3 + n
S_n_minus_1 = (n-1)**3 + (n-1)

# a_n = S_n - S_{n-1}
a_n = S_n - S_n_minus_1
a_n_simplified = simplify(expand(a_n))

# a_4 계산
a_4 = a_n_simplified.subs(n, 4)

# 검증: a_4가 38인지 확인
if a_4 == 38:
    # 조건 검증: S_4 = a_1 + a_2 + a_3 + a_4
    S_4 = 4**3 + 4  # = 68
    a_1 = (1**3 + 1) - 0  # = 2
    a_2 = (2**3 + 2) - (1**3 + 1)  # = 10 - 2 = 8
    a_3 = (3**3 + 3) - (2**3 + 2)  # = 30 - 10 = 20
    sum_check = a_1 + a_2 + a_3 + 38
    if sum_check == S_4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')