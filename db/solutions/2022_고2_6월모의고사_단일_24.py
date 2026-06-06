from sympy import symbols, simplify, Rational

x = symbols('x', real=True)

# 원래 부등식: (1/5)^(x-1) <= 5^(7-2x)
# 답: x <= 6, 자연수이므로 x in {1,2,3,4,5,6} -> 개수 6

# 검증: x=1부터 x=7까지 부등식 만족 확인
for x_val in range(1, 8):
    lhs = (Rational(1, 5)) ** (x_val - 1)
    rhs = 5 ** (7 - 2*x_val)
    is_satisfied = lhs <= rhs
    print(f'x={x_val}: {lhs} <= {rhs} : {is_satisfied}')

# 마지막 확인: x <= 6을 만족하는 자연수 개수
natural_numbers = [i for i in range(1, 7) if i <= 6]
count = len(natural_numbers)
print(f'\n자연수 개수: {count}')
if count == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')