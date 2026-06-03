import sympy as sp
k = sp.Symbol('k', integer=True)
x = sp.Symbol('x')

# 조건 (가): k^2 - 12k < 0
cond_ga = k**2 - 12*k < 0
print(f'조건 (가): {cond_ga}')

# 조건 (나): k^2 - 10k + 16 >= 0
cond_na = k**2 - 10*k + 16 >= 0
print(f'조건 (나): {cond_na}')

# 정수 k 확인 (1~11)
valid_k = []
for k_val in range(1, 12):
    ga_check = k_val**2 - 12*k_val < 0
    na_check = k_val**2 - 10*k_val + 16 >= 0
    if ga_check and na_check:
        valid_k.append(k_val)

print(f'조건을 만족하는 정수 k: {valid_k}')
print(f'개수: {len(valid_k)}')
if len(valid_k) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')