import sympy as sp

# 등차수열 {a_n}에서 a_n = a_1 + (n-1)*d
a1, d = sp.symbols('a1 d')

# 주어진 조건
# a_3 = 6
cond1 = sp.Eq(a1 + 2*d, 6)

# 2*a_5 - a_4 = 15
a5 = a1 + 4*d
a4 = a1 + 3*d
cond2 = sp.Eq(2*a5 - a4, 15)

# 연립방정식 풀이
solution = sp.solve([cond1, cond2], [a1, d])
a1_val = solution[a1]
d_val = solution[d]

# a_11 계산
a11 = a1_val + 10*d_val

# 검증
a3_check = a1_val + 2*d_val
a5_check = a1_val + 4*d_val
a4_check = a1_val + 3*d_val
cond2_check = 2*a5_check - a4_check

if a3_check == 6 and cond2_check == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')