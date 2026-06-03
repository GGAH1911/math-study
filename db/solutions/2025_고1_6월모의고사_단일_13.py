import sympy as sp
x = sp.Symbol('x')
alpha, beta = sp.symbols('alpha beta')

# 원래 이차방정식의 근
original_eq = x**2 - 7*x + 5
roots = sp.solve(original_eq, x)
alpha_val = roots[0]
beta_val = roots[1]

# 구한 P(x)
P = lambda t: t**2 - 2*t + 3

# 조건 검증
cond1 = P(alpha_val) - (5*alpha_val - 2)
cond2 = P(beta_val) - (5*beta_val - 2)

cond1_simplified = sp.simplify(cond1)
cond2_simplified = sp.simplify(cond2)

# P(5) 계산
result = P(5)

# 검증
if cond1_simplified == 0 and cond2_simplified == 0 and result == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')