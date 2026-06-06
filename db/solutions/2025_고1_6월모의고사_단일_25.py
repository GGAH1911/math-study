import sympy as sp
a = -1
result = (sp.sqrt(-4*a) / (sp.sqrt(a)*sp.sqrt(-4))) - (sp.sqrt(-32)*sp.sqrt(4*a) / (sp.sqrt(2)*sp.sqrt(-a)))
result_simplified = sp.simplify(result)
if result_simplified == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')