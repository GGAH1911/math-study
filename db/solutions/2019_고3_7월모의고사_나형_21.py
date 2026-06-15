from sympy import symbols, solve, Poly

# a = 7 검증
a = 7

# f(t) 결정함수
def get_f(t, a):
    # 3p^3 - ap^2 + (t+5) = 0의 실근 개수
    p = symbols('p', real=True)
    h = 2*p**3 - a*p**2 + (t+5)
    h_prime = 6*p**2 - 2*a*p
    
    # 극값
    h_0 = t + 5
    h_a3 = -a**3/27 + t + 5
    
    critical_t = a**3/27 - 5
    
    if -5 < t < critical_t:
        return 3
    elif t == -5 or t == critical_t:
        return 2
    else:
        return 1

# f(1), f(2), f(3) 확인
f1 = get_f(1, 7)
f2 = get_f(2, 7)
f3 = get_f(3, 7)

# 임계값 확인
crit = 7**3/27 - 5
f_crit_minus = get_f(3.0, 7)  # 3 < 208/27
f_crit_at = get_f(crit, 7)

# g(7) 계산
if f1 == f2 == f3 == 3:
    g7 = f3  # g(7) = f(f(7)) = f(3)
    result = 7 + g7
    if result == 10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')