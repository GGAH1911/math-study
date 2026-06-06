def solve(
    f_coeff_a=-1,
    f_coeff_b=2,
    f_coeff_c=-1,
    eval_point=2,
    log_rhs_constant=8,
    ineq_coefficient=4,
    target_count=6,
    max_k_search=30
):
    """
    f(x) = f_coeff_a*x^2 + f_coeff_b*x + f_coeff_c
    
    조건 (가): log_{2^k}(f(eval_point) + |k|) <= log_{2^k}(log_rhs_constant)
    조건 (나): log_{2^k}(f(x) + |k|(x-1)) <= log_{2^k}(ineq_coefficient*x)를 만족하는
              자연수 x의 개수가 target_count
    """
    
    def f(x):
        return f_coeff_a * x**2 + f_coeff_b * x + f_coeff_c
    
    # f(eval_point) 계산
    f_eval = f(eval_point)
    
    def count_condition_b(k):
        """조건 (나) 만족하는 자연수 개수"""
        if k > 0:
            # g(t) = t^2 - (k - ineq_coefficient)t + ineq_coefficient >= 0인 t
            # t ∈ {1, 2, ..., k-1}
            count = sum(1 for t in range(1, k)
                       if t**2 - (k - ineq_coefficient)*t + ineq_coefficient >= 0)
        else:
            n = abs(k)
            # g(t) = t^2 - (n - ineq_coefficient)t + ineq_coefficient <= 0인 t
            # t ∈ {1, 2, ..., n-1}
            count = sum(1 for t in range(1, n)
                       if t**2 - (n - ineq_coefficient)*t + ineq_coefficient <= 0)
        return count
    
    valid_k_list = []
    
    # k > 0 케이스
    # 조건 (가): f_eval + k <= log_rhs_constant
    # 진수 조건: f_eval + k > 0
    for k in range(1, max_k_search):
        if f_eval + k > 0 and f_eval + k <= log_rhs_constant:
            if count_condition_b(k) == target_count:
                valid_k_list.append(k)
    
    # k < 0 케이스
    # 조건 (가): f_eval + |k| >= log_rhs_constant
    # 진수 조건: f_eval + |k| > 0
    for k in range(-max_k_search, 0):
        n = abs(k)
        if f_eval + n > 0 and f_eval + n >= log_rhs_constant:
            if count_condition_b(k) == target_count:
                valid_k_list.append(k)
    
    return sum(valid_k_list)


CANDIDATE = 5
result = solve()
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')