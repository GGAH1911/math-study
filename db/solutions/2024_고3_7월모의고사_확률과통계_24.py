P_A = 2/3
P_B = (1/2) / P_A
P_Ac = 1 - P_A

cond1 = abs(P_A * P_B - 1/2) < 1e-9
cond2 = abs(P_Ac * P_B - 1/4) < 1e-9

if cond1 and cond2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')