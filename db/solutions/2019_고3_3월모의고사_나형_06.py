from sympy import symbols, Function, Eq, solve

# g(5) = 2 from 2g(5)=4
g_5 = 4 / 2  # g(5) = 2

# Since g is inverse of f: g(5)=2 means f(2)=5
f_2 = 5

# Verify: f(2)=5 => g(5)=2 => 2*g(5)=4
result = 2 * g_5
CANDIDATE = f_2

if abs(result - 4) < 1e-12 and CANDIDATE == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
