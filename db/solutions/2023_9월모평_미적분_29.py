import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 원래 문제의 조건 검증
# t = 2일 때 s = 0이 되는지 확인

def verify():
    # s = 0일 때 t = 2인지 확인
    s = 0
    e_s = np.exp(s)
    t_calc = s + (e_s + 1) * (e_s + s)
    
    # t = 2 확인
    assert abs(t_calc - 2.0) < 1e-10, f"t should be 2, got {t_calc}"
    
    # g(2) = 1 확인 (f(s) = e^s + s = 1)
    f_s = e_s + s
    assert abs(f_s - 1.0) < 1e-10, f"g(2) = f(0) should be 1, got {f_s}"
    
    # h'(1) = 3 검증을 위해 g'(2) = 1/3 확인
    # g'(t) = (e^s + 1) / (dt/ds)
    dt_ds = 2 + 2*e_s**2 + s*e_s + 2*e_s
    g_prime = (e_s + 1) / dt_ds
    
    expected_g_prime = 1/3
    assert abs(g_prime - expected_g_prime) < 1e-10, f"g'(2) should be 1/3, got {g_prime}"
    
    # h'(1) = 1/g'(2) = 3
    h_prime_1 = 1 / g_prime
    assert abs(h_prime_1 - 3.0) < 1e-10, f"h'(1) should be 3, got {h_prime_1}"
    
    print("VERIFY_PASS")

verify()