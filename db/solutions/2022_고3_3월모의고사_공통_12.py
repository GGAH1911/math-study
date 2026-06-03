from sympy import symbols, expand, factor, simplify, limit, oo

x, a, r = symbols('x a r', real=True)

# Define f(x)
def f_left(x_val):
    return x_val**2 - 4*x_val + 3

def f_right(x_val, a_val):
    return -x_val**2 + a_val*x_val

# With a=4, r=2
a_val = 4
r_val = 2

# Define g(x) = (x-1)(x-4)(x-2)
def g(x_val):
    return (x_val - 1) * (x_val - 4) * (x_val - 2)

# h(1): x=1 is in domain x<=2
# h(x) = g(x)/f(x) = [(x-1)(x-4)(x-2)] / [(x-1)(x-3)]
# Cancel (x-1): = [(x-4)(x-2)] / (x-3)
h_1_limit = ((1-4)*(1-2)) / (1-3)
print(f"h(1) = {h_1_limit}")

# h(3): x=3 is in domain x>2
# f(3) = -9 + 4*3 = 3
# g(3) = (3-1)(3-4)(3-2) = 2*(-1)*1 = -2
h_3 = g(3) / f_right(3, a_val)
print(f"h(3) = {h_3}")

# h(1) + h(3)
result = h_1_limit + h_3
print(f"h(1) + h(3) = {result}")

# Expected answer: -13/6
expected = -13/6
print(f"Expected: {expected}")
print(f"Match: {abs(result - expected) < 1e-10}")

if abs(result - expected) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")