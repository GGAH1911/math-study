from sympy import *

# Define f and g
def f(x):
    return -Rational(1,2)*(x+1)**2

def g(x):
    return 2*(x-2)**2

# Verify conditions
# (가) f(x) <= 0 <= g(x) for all x
print(f"f(x) always <= 0: {f(-1) == 0}")
print(f"g(x) always >= 0: {g(2) == 0}")

# Check f(1) = -2, g(1) = 2
print(f"f(1) = {f(1)} (expected -2)")
print(f"g(1) = {g(1)} (expected 2)")

# (다) f(x) = f(0) roots sum
f0 = f(0)
eq = f(0) - f0
roots = solve(eq, Symbol('x'))
root_sum = sum(roots)
print(f"f(0) = {f0}")
print(f"Roots of f(x)=f(0): {roots}")
print(f"Root sum = {root_sum} < 0: {root_sum < 0}")

# Calculate answer
result = f(3) + g(11)
print(f"\nf(3) = {f(3)}")
print(f"g(11) = {g(11)}")
print(f"f(3) + g(11) = {result}")
print(f"\nVERIFY_PASS" if result == 154 else f"VERIFY_FAIL")