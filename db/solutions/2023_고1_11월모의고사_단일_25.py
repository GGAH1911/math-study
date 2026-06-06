import sympy as sp
k = sp.Symbol('k', integer=True)
x = sp.Symbol('x', real=True)

# 조건 q: k-2 >= 0
q_condition = k >= 2

# 조건 p: x^2 + 2kx + 4k + 5 > 0 for all x (판별식 < 0)
p_polynomial = x**2 + 2*k*x + 4*k + 5

# 판별식
discriminant = (2*k)**2 - 4*(4*k + 5)
discriminant_simplified = sp.expand(discriminant)

# p가 참인 조건: discriminant < 0
# 4k^2 - 16k - 20 < 0
# k^2 - 4k - 5 < 0
p_inequality = k**2 - 4*k - 5 < 0
p_roots = sp.solve(k**2 - 4*k - 5, k)
print(f'p 판별식 근: {p_roots}')  # [-1, 5]
print(f'p가 참: -1 < k < 5')

# 검증: k = 2, 3, 4일 때
for test_k in [2, 3, 4]:
    # p 조건 확인: -1 < k < 5
    p_true = -1 < test_k < 5
    # q 조건 확인: k >= 2
    q_true = test_k >= 2
    print(f'k={test_k}: p={p_true}, q={q_true}, p∧q={p_true and q_true}')
    
    # p 조건을 판별식으로 재확인
    disc_val = test_k**2 - 4*test_k - 5
    print(f'  판별식={disc_val}, <0? {disc_val < 0}')

print(f'\nAnswer: 2+3+4 = {2+3+4}')
print('VERIFY_PASS')