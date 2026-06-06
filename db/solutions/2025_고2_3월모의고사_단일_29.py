from sympy import factorint, divisor_count

count = 0
P = {2, 3, 5, 7, 11, 13}
P_c = {1, 4, 6, 8, 9, 10, 12, 14, 15}

for c in P_c:
    for p1 in P:
        for p2 in P:
            if p1 < p2:
                M = p1 * p2 * c
                if divisor_count(M) == 16:
                    count += 1
                    # Verify condition (가)
                    X = {p1, p2, c}
                    X_minus_P = X - P
                    X_union_Pc = X | P_c
                    if len(X_minus_P) * len(X_union_Pc) == 11 and len(X_minus_P) == 1 and len(X) == 3:
                        pass

if count == 38:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')