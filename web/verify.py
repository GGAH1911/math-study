import sympy as sp

# Let's verify the vertex and points for y = (x - 2)^2 + 1
x = sp.Symbol('x')
y = (x - 2)**2 + 1

# Vertex is at x=2, y=1
v_x = 2
v_y = y.subs(x, 2)
print(f"Vertex: ({v_x}, {v_y})")

# Let's check coordinates at boundaries of tRange [0.2, 3.8]
x_min = 0.2
x_max = 3.8
y_min = y.subs(x, x_min)
y_max = y.subs(x, x_max)
print(f"y at {x_min}: {y_min}")
print(f"y at {x_max}: {y_max}")

