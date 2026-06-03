from sympy import symbols, simplify, Matrix

# 벡터 성분으로 검증: 임의의 벡터 a, b를 설정
a_x, a_y, b_x, b_y, k = symbols('a_x a_y b_x b_y k', real=True)

# 벡터 정의
A = Matrix([a_x, a_y])
B = Matrix([b_x, b_y])

# 주어진 식의 좌변
LHS = A + 3*(A - B)

# 주어진 식의 우변
RHS = k*A - 3*B

# k=4일 때 검증
RHS_k4 = RHS.subs(k, 4)

result = simplify(LHS - RHS_k4)
if all(result[i] == 0 for i in range(len(result))):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')