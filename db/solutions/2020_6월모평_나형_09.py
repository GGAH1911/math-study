from sympy import symbols, Eq, solve

# 수열 항들을 기호로 정의 (a_1부터 a_5까지)
a_symbols = [symbols(f'a{i}') for i in range(1, 6)]

# 방정식 리스트
equations = []

# 초기 조건: a_1 = 1
equations.append(Eq(a_symbols[0], 1))

# 점화식: a_{n+1} + (-1)^n * a_n = 2^n
# n=1,2,3,4에 대해 원래 식 그대로 코드화
for n in range(1, 5):
    # a_symbols[0]=a_1, a_symbols[1]=a_2, ..., a_symbols[4]=a_5
    # 점화식: a_{n+1} + (-1)^n * a_n = 2^n
    eq = Eq(a_symbols[n] + ((-1)**n) * a_symbols[n-1], 2**n)
    equations.append(eq)

# 방정식계 풀기
solution = solve(equations, a_symbols)

# a_5의 값 추출
a5_value = solution[a_symbols[4]]
print(f"a_5 = {a5_value}")

# 검증: 도출된 답이 모든 원래 조건을 만족하는지 확인
verification_passed = True

# 초기 조건 확인
if solution[a_symbols[0]] != 1:
    verification_passed = False

# 점화식 각각 확인 (원래 식 재대입)
for n in range(1, 5):
    lhs = solution[a_symbols[n]] + ((-1)**n) * solution[a_symbols[n-1]]
    rhs = 2**n
    if lhs != rhs:
        verification_passed = False

if verification_passed:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")