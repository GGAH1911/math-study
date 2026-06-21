from sympy import symbols, solve, Eq

# 공차 d와 첫째항 a1을 변수로 정의
a1, d = symbols('a1 d', real=True)

# 등차수열: a_n = a1 + (n-1)*d
# 조건 1: a1 + a2 + a3 = 15
cond1 = Eq(a1 + (a1 + d) + (a1 + 2*d), 15)

# 조건 2: a3 + a4 + a5 = 39
cond2 = Eq((a1 + 2*d) + (a1 + 3*d) + (a1 + 4*d), 39)

# 연립방정식 풀기
sol = solve([cond1, cond2], [a1, d])

# 공차 d 확인
public_d = sol[d]

# 검증: 조건을 만족하는지 확인
a1_val = sol[a1]
seq = [a1_val + (n-1)*public_d for n in range(1, 6)]
sum123 = seq[0] + seq[1] + seq[2]
sum345 = seq[2] + seq[3] + seq[4]

if sum123 == 15 and sum345 == 39 and public_d == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')