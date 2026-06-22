import sympy as sp

x = sp.Symbol('x')
y1 = -0.3*(x-2)**2 + 3
y2 = 0.2*(x-2)**2 + 3
y3 = 0.5/(7-x) + 1.5
y4 = 0.5/(x-7) + 1.5

print("y1(0.5):", float(y1.subs(x, 0.5)))
print("y1(2):", float(y1.subs(x, 2)))
print("y2(2):", float(y2.subs(x, 2)))
print("y2(4):", float(y2.subs(x, 4)))
print("y3(4):", float(y3.subs(x, 4)))
print("y3(6.92):", float(y3.subs(x, 6.92)))
print("y4(7.08):", float(y4.subs(x, 7.08)))
print("y4(9.5):", float(y4.subs(x, 9.5)))
