import sympy as sp
sqrt6 = sp.sqrt(6)

MH = sqrt6 + 1
NH = sqrt6 - 1

MH_cubed = MH**3
NH_cubed = NH**3
result = MH_cubed + NH_cubed
result_simplified = sp.simplify(result)

expected = 18 * sqrt6

if sp.simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')