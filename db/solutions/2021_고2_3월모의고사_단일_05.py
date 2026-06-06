from sympy import symbols, discriminant, solve
a = symbols('a', real=True)
eq = a**2 - 64
for a_val in [7, 8, 9]:
    disc = a_val**2 - 64
    print(f'a={a_val}: discriminant={disc}', '허근' if disc < 0 else '허근아님')
if 7**2 < 64 and 8**2 >= 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')