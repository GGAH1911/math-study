from sympy import symbols, Function, diff, Eq, solve, Rational

x = symbols('x')

# We need f'(0)+g'(0) = 2
# Verify via the original equation identity
# (x+1)f(x) + (1-x)g(x) = x^3 + 9x + 1, f(0)=4

# From x=0: f(0)+g(0)=1, f(0)=4 => g(0)=-3
f0 = 4
g0_val = 1 - f0  # = -3

# Differentiate: f(x)+(x+1)f'(x) - g(x)+(1-x)g'(x) = 3x^2+9
# At x=0: f(0)+f'(0) - g(0)+g'(0) = 9
# 4 + f'(0) - (-3) + g'(0) = 9
# f'(0)+g'(0) = 9 - 4 - 3 = 2

result = 9 - f0 - (-g0_val)  # 9 - f(0) + g(0) but sign: 9 - f(0) + g(0)
# Let me redo: f(0) + f'0 - g(0) + g'0 = 9
# f'0 + g'0 = 9 - f(0) + g(0)
fp_plus_gp = 9 - f0 + g0_val  # 9 - 4 + (-3) = 2

assert fp_plus_gp == 2, f'Expected 2, got {fp_plus_gp}'
print('VERIFY_PASS')
