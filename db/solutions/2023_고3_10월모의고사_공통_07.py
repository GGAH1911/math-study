from sympy import symbols, solve, simplify

# 등차수열 정의: a_n = a_1 + (n-1)*d
a1, d = symbols('a1 d', real=True)

# 합 공식: S_n = n*a_1 + n(n-1)/2 * d
def S(n):
    return n*a1 + n*(n-1)//2 * d

# 조건들
eq1 = S(7) - S(4)  # = 0
eq2 = S(6) - 30    # = 0

# 연립방정식 풀이
sol = solve([eq1, eq2], [a1, d])

# a_2 계산
a1_val = sol[a1]
d_val = sol[d]
a2_val = a1_val + d_val

# 검증
S4 = 4*a1_val + 4*3//2*d_val
S6 = 6*a1_val + 6*5//2*d_val
S7 = 7*a1_val + 7*6//2*d_val

cond1_check = S7 - S4
cond2_check = S6 - 30

if abs(cond1_check) < 1e-10 and abs(cond2_check) < 1e-10 and a2_val == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')