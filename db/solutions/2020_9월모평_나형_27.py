from sympy import symbols, expand, factor, solve, simplify

CANDIDATE = 21

x, k = symbols('x k', real=True)

# 원래 곡선 함수
def curve(x_val):
    return x_val**3 - 3*x_val**2 + 2*x_val - 3

# 직선 함수
def line(x_val, k_val):
    return 2*x_val + k_val

# k = -3인 경우
k1 = -3
h1 = x**3 - 3*x**2 - (3 + k1)
factored1 = factor(h1)
roots1 = solve(h1, x)
print(f'k = -3: h(x) = {factored1}, roots = {roots1}')

# k = -7인 경우
k2 = -7
h2 = x**3 - 3*x**2 - (3 + k2)
factored2 = factor(h2)
roots2 = solve(h2, x)
print(f'k = -7: h(x) = {factored2}, roots = {roots2}')

# k 값들의 곱
product_k = k1 * k2
print(f'Product of k values: {product_k}')

if product_k == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')