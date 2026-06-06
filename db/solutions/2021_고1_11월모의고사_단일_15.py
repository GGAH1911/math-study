import sympy as sp
x, k = sp.symbols('x k')

# Case k = -2
ineq1 = x**2 - 2*x - 3
ineq2_k_minus2 = x**2 - 3*x - 10
roots1 = sp.solve(ineq1, x)
roots2_k_minus2 = sp.solve(ineq2_k_minus2, x)

# Find integer solutions for k = -2
integers_k_minus2 = []
for i in range(-10, 10):
    if ineq1.subs(x, i) >= 0 and ineq2_k_minus2.subs(x, i) <= 0:
        integers_k_minus2.append(i)

# Case k = 9
ineq2_k_9 = x**2 - 14*x + 45
integers_k_9 = []
for i in range(-10, 15):
    if ineq1.subs(x, i) >= 0 and ineq2_k_9.subs(x, i) <= 0:
        integers_k_9.append(i)

count_k_minus2 = len(integers_k_minus2)
count_k_9 = len(integers_k_9)
product = (-2) * 9

if count_k_minus2 == 5 and count_k_9 == 5 and product == -18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')