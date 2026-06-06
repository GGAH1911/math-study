from sympy import symbols, solve, Abs

# 가능한 모든 (a,b,c,d) 조합 확인
results = []

for a in range(1, 10):
    for b in range(1, 10):
        if a**2 + b**2 != 10:
            continue
        
        for c in range(1, 10):
            for d in range(1, 10):
                z1_squared = a**2 + b**2
                z2_squared = c**2 + d**2
                z1_plus_z2_squared = (a + c)**2 + (b + d)**2
                
                if z1_plus_z2_squared == 41:
                    results.append({'a':a, 'b':b, 'c':c, 'd':d, 'z2_sq':z2_squared})

# 최댓값 확인
max_z2_sq = max(r['z2_sq'] for r in results)
assert max_z2_sq == 17, f"Expected max=17, got {max_z2_sq}"

# ㄴ 검증: z_1 + conj(z_2) = 3일 때
for r in results:
    a, b, c, d = r['a'], r['b'], r['c'], r['d']
    z1_plus_conj_z2_real = a + c
    z1_plus_conj_z2_imag = b - d
    
    if z1_plus_conj_z2_real == 3 and z1_plus_conj_z2_imag == 0:
        assert c + d == 5, f"When z1+conj(z2)=3, expected c+d=5 but got {c+d}"

print('VERIFY_PASS')