import sympy as sp
k = sp.Symbol('k', positive=True, real=True)

# Test each k value
k_values = [2, sp.sqrt(2), 2*sp.sqrt(3)/3, sp.sqrt(6)/3]
k2_sum = 0

for k_val in k_values:
    # Case 1-1-2: k=2
    if k_val == 2:
        a = [k_val, k_val/3, -k_val/3, k_val**2/3, k_val**2/3 - 2*k_val/3]
        assert a[4] == 0, f'k=2: a_5 should be 0'
        assert a[1] * a[2] < 0, f'k=2: a_2*a_3 should be negative'
        k2_sum += k_val**2
    
    # Case 1-2-2: k=sqrt(2)
    elif k_val == sp.sqrt(2):
        a = [k_val, k_val/3, -k_val**2/3, k_val**3/3, k_val**3/3 - 2*k_val/3]
        a5_check = sp.simplify(a[4])
        assert a5_check == 0, f'k=sqrt(2): a_5 should be 0, got {a5_check}'
        a2a3 = sp.simplify(a[1] * a[2])
        assert a2a3 < 0, f'k=sqrt(2): a_2*a_3 should be negative'
        k2_sum += k_val**2
    
    # Case 2-1 (option 1): k=2*sqrt(3)/3
    elif k_val == 2*sp.sqrt(3)/3:
        a = [k_val, -k_val**2, k_val**3, k_val**3 - 2*k_val/3, k_val**3 - 4*k_val/3]
        a5_check = sp.simplify(a[4])
        assert a5_check == 0, f'k=2√3/3: a_5 should be 0, got {a5_check}'
        a2a3 = sp.simplify(a[1] * a[2])
        assert a2a3 < 0, f'k=2√3/3: a_2*a_3 should be negative'
        k2_sum += k_val**2
    
    # Case 2-1 (option 2): k=sqrt(6)/3
    elif k_val == sp.sqrt(6)/3:
        a = [k_val, -k_val**2, k_val**3, k_val**3 - 2*k_val/3]
        a4_check = sp.simplify(a[3])
        a5 = -k_val * a4_check
        a5_check = sp.simplify(a5)
        assert a5_check == 0, f'k=√6/3: a_5 should be 0, got {a5_check}'
        a2a3 = sp.simplify(a[1] * a[2])
        assert a2a3 < 0, f'k=√6/3: a_2*a_3 should be negative'
        k2_sum += k_val**2

result_sum = sp.simplify(k2_sum)
assert result_sum == 8, f'Sum should be 8, got {result_sum}'
print('VERIFY_PASS')