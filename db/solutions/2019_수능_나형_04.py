from sympy import Eq

CANDIDATE = 3

choices = [3, 4, 5, 6, 7]
expected_value = choices[CANDIDATE - 1]

f = {1: 2, 2: 3, 3: 4, 4: 1}

f_4 = f[4]
f_f_2 = f[f[2]]
result = f_4 + f_f_2

eq = Eq(result, expected_value)

if eq:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")