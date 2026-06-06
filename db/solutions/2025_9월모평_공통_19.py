from sympy import symbols, solve, simplify

CANDIDATE = '4'
a_val = int(CANDIDATE)

# Define symbolic variable for unknown coefficient
b = symbols('b', real=True)

# Given function: f(x) = a*x^3 + b*x^2 + c*x + 9
# Condition 1: x=1 is a local minimum, so f'(1) = 0
# f'(x) = 3*a*x^2 + 2*b*x + c
# 3*a + 2*b + c = 0
# Therefore: c = -3*a - 2*b

c_expr = -3*a_val - 2*b

# Analyze critical points:
# f'(x) = 3*a*x^2 + 2*b*x + c
#       = 3*a*x^2 + 2*b*x + (-3*a - 2*b)
#       = 3*a(x^2 - 1) + 2*b(x - 1)
#       = (x - 1)[3*a*(x + 1) + 2*b]
# Critical points: x = 1 and x = -1 - 2*b/(3*a)
# Since x=1 is local minimum, x_max = -1 - 2*b/(3*a) must be local maximum

x_max = -1 - 2*b/(3*a_val)

# Condition 2: Maximum value is 28
# f(x_max) = 28
f_at_xmax = a_val*x_max**3 + b*x_max**2 + c_expr*x_max + 9

# Set up equation: f(x_max) = 28
equation = f_at_xmax - 28
equation_simplified = simplify(equation)

# Solve for b
solutions_b = solve(equation_simplified, b)

# Verify: check if real solutions exist
has_real_solution = False

if solutions_b:
    for sol in solutions_b:
        try:
            # Check if solution can be interpreted as real
            val_float = float(sol)
            has_real_solution = True
            break
        except (TypeError, AttributeError):
            try:
                val_complex = complex(sol)
                if abs(val_complex.imag) < 1e-10:
                    has_real_solution = True
                    break
            except:
                pass

if has_real_solution:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")