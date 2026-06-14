from sympy import symbols, binomial, simplify, expand
k = symbols('k', positive=True, integer=True)

CANDIDATE = 135

# f(k) = C(k,2) = k(k-1)/2
f_k = k * (k - 1) / 2
f_10 = f_k.subs(k, 10)

# g(k) = k(k+1)
g_k = k * (k + 1)
g_9 = g_k.subs(k, 9)

# Sum
result = f_10 + g_9
result_value = int(result)

if result_value == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')