from sympy import symbols, Eq, solve as sym_solve, simplify

def solve(lower_n_coeff=2, lower_const=-12,
          upper_n2_coeff=4, upper_n_coeff=-2, upper_const=-12):
    """
    부등식 lower_n_coeff*n + lower_const <= (f(n)-n^2)/(n-2) <= upper_n2_coeff*n^2 + upper_n_coeff*n + upper_const
    에서 f(x) = x^3 + ax^2 + bx + c (최고차 계수=1)의 a, b를 구하고 f'(3)을 반환.
    
    기본값: 원문제 (정답=31)
    """
    
    # k = n - 2 변환
    L0 = 2 * lower_n_coeff + lower_const
    L1 = lower_n_coeff
    
    U2 = upper_n2_coeff
    U1 = 4 * upper_n2_coeff + upper_n_coeff
    U0 = 4 * upper_n2_coeff + 2 * upper_n_coeff + upper_const
    
    # 상·하한이 만나는 점 찾기: U2*k^2 + (U1-L1)*k + (U0-L0) = 0
    k = symbols('k')
    diff_eq = U2 * k**2 + (U1 - L1) * k + (U0 - L0)
    roots = sym_solve(diff_eq, k)
    
    k1, k2 = roots[0], roots[1]
    
    # a, b 구하기
    # g(k) = [f(k+2) - f(k)]/2 = 3k^2 + (6+2a)k + (4+2a+b)
    # 등호 조건: g(k1) = L0 + L1*k1, g(k2) = L0 + L1*k2
    a, b = symbols('a b')
    
    eq1 = Eq(3*k1**2 + (6 + 2*a)*k1 + (4 + 2*a + b), L0 + L1*k1)
    eq2 = Eq(3*k2**2 + (6 + 2*a)*k2 + (4 + 2*a + b), L0 + L1*k2)
    
    solution = sym_solve([eq1, eq2], [a, b])
    a_val = solution[a]
    b_val = solution[b]
    
    # f'(x) = 3x^2 + 2ax + b에서 f'(3) = 27 + 6a + b
    result = 27 + 6*a_val + b_val
    result = simplify(result)
    
    return result


CANDIDATE = '31'
result = solve()
print('VERIFY_PASS' if str(result) == CANDIDATE else 'VERIFY_FAIL')