from sympy import symbols, Eq, solve
a = symbols('a')
# A(a,4,-9), B(1,0,-3), 3:1 외분점
m, n = 3, 1
Px = (m*1 - n*a) / (m - n)
Pz = (m*(-3) - n*(-9)) / (m - n)
# y축 위 조건: x=0, z=0
sol = solve([Eq(Px, 0), Eq(Pz, 0)], a)
print('VERIFY_PASS' if sol and sol[a] == 3 else 'VERIFY_FAIL')
