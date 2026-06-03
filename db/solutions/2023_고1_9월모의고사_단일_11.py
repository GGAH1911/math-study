from sympy import symbols, expand, solve, Eq

x, y = symbols('x y')

# Given answer values
a = 2
b = -4

# Step 1: Verify vertex of quadratic y = x^2 - 4x + a
# Vertex x-coordinate: x = -(-4)/(2*1) = 2
vertex_x = 2
vertex_y = vertex_x**2 - 4*vertex_x + a  # = 4 - 8 + 2 = -2

# Step 2: Find center of circle x^2 + y^2 + bx + 4y - 17 = 0
# Complete the square:
# (x + b/2)^2 - b^2/4 + (y + 2)^2 - 4 - 17 = 0
center_x = -b / 2  # = -(-4)/2 = 2
center_y = -2

# Step 3: Check vertex == center
vertex_matches_center = (vertex_x == center_x) and (vertex_y == center_y)

# Step 4: Check radius^2 > 0 (valid circle)
radius_sq = 21 + b**2 / 4  # = 21 + 4 = 25

if vertex_matches_center and radius_sq > 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: vertex=({vertex_x},{vertex_y}), center=({center_x},{center_y}), r^2={radius_sq}')
