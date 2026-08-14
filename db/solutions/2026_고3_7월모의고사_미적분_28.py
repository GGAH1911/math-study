import sympy as sp
from sympy import exp, ln, integrate, symbols, diff, solve, N

x, t = symbols('x t', real=True)

# Define f(x)
f = lambda z: z - 1/(exp(z) + 1)

# f(0) and f(1)
f0 = f(0)
f1 = f(1)

print(f"f(0) = {f0} = {N(f0)}")
print(f"f(1) = {f1} = {N(f1)}")

# Define g(x) = ln(x) - 1/(x+1)
g = lambda z: ln(z) - 1/(z + 1)

# Verify g(1) = f(0) and g(e) = f(1)
g1 = g(1)
ge = g(exp(1))

print(f"\ng(1) = {g1}")
print(f"f(0) = {f0}")
print(f"Match: {sp.simplify(g1 - f0) == 0}")

print(f"\ng(e) = {ge}")
print(f"f(1) = {f1}")
print(f"Match: {sp.simplify(ge - f1) == 0}")

# Compute integral of f from 0 to 1
integral_f01 = integrate(f(t), (t, 0, 1))
print(f"\n∫₀¹ f(t) dt = {integral_f01}")

# Compute integral of g from 1 to e
integral_g1e = integrate(g(t), (t, 1, exp(1)))
print(f"∫₁ᵉ g(t) dt = {integral_g1e}")

# Sum
sum_integrals = integral_f01 + integral_g1e
print(f"\nSum = {sum_integrals} = {N(sum_integrals)}")
print(f"Simplified: {sp.simplify(sum_integrals)}")

# Final answer: f(1)*(1+e) - f(0) - 1/2
result = f1 * (1 + exp(1)) - f0 - sp.Rational(1,2)
result_simplified = sp.simplify(result)

print(f"\nFinal answer: {result_simplified}")
print(f"Numeric value: {N(result_simplified)}")

if sp.simplify(result_simplified - exp(1)) == 0:
    print("\nVERIFY_PASS")
else:
    print("\nVERIFY_FAIL")