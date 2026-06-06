import sympy as sp

# k의 조건을 만족하는 실근 구하기
k = sp.Symbol('k', real=True)
eq = k - 3/k - 6
k_solutions = sp.solve(eq, k)
print(f'k 해: {k_solutions}')

# 각 k값에 대해 검증
for k_val in k_solutions:
    # 조건 확인
    cond_check = float(k_val - 3/k_val)
    print(f'\nk = {k_val}')
    print(f'k - 3/k = {cond_check} (should be 6)')
    
    # 목표 값 계산
    result = k_val**3 - 27/k_val**3
    result_simplified = sp.simplify(result)
    print(f'k^3 - 27/k^3 = {result_simplified}')

# 답 검증 (270이 맞는지)
print(f'\nFinal answer verification:')
for k_val in k_solutions:
    target = k_val**3 - 27/k_val**3
    if abs(float(target) - 270) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')