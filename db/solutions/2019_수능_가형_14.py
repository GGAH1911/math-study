from sympy import symbols, expand, factor, Rational

# 변수 정의
x = symbols('x', real=True)

# 그래프에서 정의된 함수들
# f(x) = (x-2)(x-4): 이차함수, 근이 2와 4
f_x = (x - 2) * (x - 4)

# g(x) = (3/2)(x-3): 일차함수, x=3에서 0
g_x = Rational(3, 2) * (x - 3)

print("="*60)
print("부등식: (1/2)^(f(x)*g(x)) >= (1/8)^(g(x))")
print("="*60)

# 부등식 변환
print("\n[변환 과정]")
print("(1/8)^(g(x)) = (1/2)^(3*g(x))")
print("(1/2)^(f(x)*g(x)) >= (1/2)^(3*g(x))")
print("밑 1/2 < 1이므로 지수 부등호 뒤집기:")
print("f(x)*g(x) <= 3*g(x)")
print("g(x)*[f(x) - 3] <= 0")

# 함수 전개 및 인수분해
f_x_expanded = expand(f_x)
f_x_minus_3 = expand(f_x - 3)
f_x_minus_3_factored = factor(f_x_minus_3)

print("\n[함수 분석]")
print(f"f(x) = {f_x_expanded}")
print(f"g(x) = {g_x}")
print(f"f(x) - 3 = {f_x_minus_3_factored}")

print("\n[부등식 정리]")
print("g(x) * (f(x) - 3) <= 0")
print("(3/2)(x-3) * (x-1)(x-5) <= 0")
print("(x-3)(x-1)(x-5) <= 0")

# 자연수 해 찾기
print("\n[자연수 해 찾기]")
natural_number_solutions = []
for n in range(1, 10):
    product = (n - 3) * (n - 1) * (n - 5)
    if product <= 0:
        natural_number_solutions.append(n)
        print(f"x={n}: ({n-3})({n-1})({n-5})={product} <= 0 ✓")

answer = sum(natural_number_solutions)

print("\n[결과]")
print(f"부등식을 만족하는 자연수: {natural_number_solutions}")
print(f"합: {answer}")

# 검증: 원래 부등식 조건 확인
print("\n[검증: 원래 부등식 f(x)*g(x) <= 3*g(x) 확인]")
all_pass = True
for n in natural_number_solutions:
    f_val = (n - 2) * (n - 4)
    g_val = Rational(3, 2) * (n - 3)
    
    # 부등식: f(x)*g(x) <= 3*g(x)
    lhs = f_val * g_val
    rhs = 3 * g_val
    
    is_satisfied = (lhs <= rhs)
    print(f"x={n}: f({n})*g({n})={lhs}, 3*g({n})={rhs}, {lhs}<={rhs}? {is_satisfied}")
    
    if not is_satisfied:
        all_pass = False

print("\n" + "="*60)
if all_pass and answer == 13:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
print("="*60)