from sympy import symbols, Eq, solve

# 네 수가 등차수열을 이룬다
# 첫째항 = 2, 넷째항 = 14
# 등차수열의 일반항: a_n = a_1 + (n-1)*d

d = symbols('d', real=True)
# 넷째항: 2 + 3*d = 14
eq = Eq(2 + 3*d, 14)
d_val = solve(eq, d)[0]

# a와 b 계산
a_val = 2 + d_val
b_val = 2 + 2*d_val

# a + b 계산
answer = a_val + b_val

# 검증: 2, a, b, 14가 정말 등차수열인지 확인
sequence = [2, a_val, b_val, 14]
differences = [sequence[i+1] - sequence[i] for i in range(3)]

if answer == 16 and all(diff == d_val for diff in differences):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')