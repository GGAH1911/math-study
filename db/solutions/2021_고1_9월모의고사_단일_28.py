from sympy import symbols, sqrt, solve

a, b, r = symbols('a b r', real=True, positive=True)

# Condition 1: Circle passes through O(0,0)
eq1 = a**2 + b**2 - r**2

# Condition 2: Line OC has equation y = 3x
eq2 = b - 3*a

# Condition 3: OB - OA = 4, where OA = 2a, OB = 2b
eq3 = 2*b - 2*a - 4

# Solve the system
solution = solve([eq1, eq2, eq3], [a, b, r])
print(f"Solution: {solution}")

# Extract values (positive solution)
for sol in solution:
    a_val, b_val, r_val = sol
    if a_val > 0 and b_val > 0 and r_val > 0:
        r_squared = r_val**2
        answer = a_val + b_val + r_squared
        print(f"a={a_val}, b={b_val}, r²={r_squared}")
        print(f"a + b + r² = {answer}")
        
        # Verify all conditions
        verify_cond1 = a_val**2 + b_val**2 - r_squared
        verify_cond2 = b_val - 3*a_val
        verify_cond3 = 2*b_val - 2*a_val - 4
        
        print(f"Verify condition 1 (a²+b²=r²): {verify_cond1} (should be 0)")
        print(f"Verify condition 2 (b=3a): {verify_cond2} (should be 0)")
        print(f"Verify condition 3 (2b-2a=4): {verify_cond3} (should be 0)")
        
        # Verify points on circle
        circle_check_A = (2*a_val - a_val)**2 + (0 - b_val)**2 - r_squared
        circle_check_B = (0 - a_val)**2 + (2*b_val - b_val)**2 - r_squared
        circle_check_O = (0 - a_val)**2 + (0 - b_val)**2 - r_squared
        
        print(f"A on circle: {circle_check_A} (should be 0)")
        print(f"B on circle: {circle_check_B} (should be 0)")
        print(f"O on circle: {circle_check_O} (should be 0)")
        
        if abs(answer - 14) < 0.0001:
            print("VERIFY_PASS")
        else:
            print("VERIFY_FAIL")