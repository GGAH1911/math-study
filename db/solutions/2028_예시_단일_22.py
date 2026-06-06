import sympy as sp
a_vals = [2, 3, 4, 5]
for a in a_vals:
    base = 7 - a
    arg = 2*a - 3
    if base > 0 and base != 1 and arg > 0:
        log_val = sp.log(arg, base)
        if log_val >= 0:
            print(f'a={a}: log_{base}({arg}) = {float(log_val):.4f} >= 0 ✓')
        else:
            print('VERIFY_FAIL')
            exit()
print('VERIFY_PASS')