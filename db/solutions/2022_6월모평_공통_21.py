from sympy import symbols, expand, roots

CANDIDATE = 24

x = symbols('x')
valid_n_values = []

# 모든 자연수 n에 대해 조건 검증
for n in range(1, 100):
    # 조건: 64^(2/n)이 양의 정수여야 함
    # 64 = 2^6이므로 64^(2/n) = 2^(12/n)
    # 이것이 정수 ⟺ n | 12
    
    if 12 % n != 0:
        continue
    
    # 분석 결과: n은 짝수여야 함
    # (홀수 n에서는 x^n=64의 실근이 1개여서 조건 불가능)
    if n % 2 != 0:
        continue
    
    # 64^(2/n) = 2^(12/n) 계산
    exponent = 12 // n
    coeff = 2 ** exponent
    
    # f(x) = x^2 - 64^(2/n) (최고차항 계수 1, 근: ±64^(1/n))
    f_poly = x**2 - coeff
    
    # g(x) = x^n - 64
    g_poly = x**n - 64
    
    # 원래 방정식: (x^n - 64) * f(x) = 0
    combined = expand(g_poly * f_poly)
    
    # 근과 중복도 구하기
    root_dict = roots(combined, x)
    
    # 실근만 필터링 (조건 가에 필요)
    real_roots = {r: m for r, m in root_dict.items() if r.is_real}
    
    # 조건 (가) 검증
    # 1. 서로 다른 두 실근
    if len(real_roots) != 2:
        continue
    
    # 2. 각 실근이 중근 (중복도 = 2)
    if not all(mult == 2 for mult in real_roots.values()):
        continue
    
    # 조건 (나) 검증
    # f(x) = x^2 - coeff의 최솟값은 x=0에서 -coeff
    min_value = -coeff
    
    # 최솟값이 음의 정수인지 확인
    if not isinstance(coeff, int) or min_value >= 0:
        continue
    
    # 모든 조건 만족
    valid_n_values.append(n)

# 조건을 만족하는 모든 n의 합 계산
sum_of_valid_n = sum(valid_n_values)

# 원래 문제 조건으로 계산한 결과가 CANDIDATE와 일치하는지 검증
if sum_of_valid_n == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")