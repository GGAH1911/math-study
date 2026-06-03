import sympy as sp
a, b, x = sp.symbols('a b x', real=True)

# Verify the constraint equation
a_val = sp.Rational(1,2)
b_val = 2*a_val - 1
print(f'Test a={a_val}, b={b_val}: a+b={a_val+b_val}')

a_val2 = -1 - sp.sqrt(2)
b_val2 = 2*a_val2 - 1
print(f'Test a=-1-√2={a_val2}, b={b_val2}: a+b={a_val2+b_val2}')

# Check M - m
M = sp.Rational(1,2)
m = -4 - 3*sp.sqrt(2)
diff = M - m
print(f'M={M}, m={m}')
print(f'M - m = {sp.simplify(diff)}')

if sp.simplify(diff - (sp.Rational(9,2) + 3*sp.sqrt(2))) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')