from sympy import sqrt, Symbol, Eq, solve

x = Symbol('x')
a = Symbol('a')

# 원래 함수를 x축 방향으로 a만큼 평행이동
transformed = sqrt(2*(x-a))
# 목표 함수
target = sqrt(2*x - 4)

# 루트 안의 식이 같아야 함
eq = Eq(2*(x-a), 2*x - 4)
a_value = solve(eq, a)[0]

# 검증: a=2일 때 transformed = target인지 확인
transformed_result = sqrt(2*(x-a_value))
target_simplified = sqrt(2*x - 4)

# 일치하는지 확인
if transformed_result.equals(target_simplified):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')