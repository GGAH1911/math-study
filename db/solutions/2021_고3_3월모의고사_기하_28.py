from sympy import Rational

total = 0
for n in range(1, 9):
    x_n = 2*n - Rational(1, 2)
    y_n_sq = 2 * x_n  # y_n^2 = 2*x_n (parabola)
    
    # Check: FP_n = x_n + 1/2 == 2n
    FP_n = x_n + Rational(1, 2)
    assert FP_n == 2*n, f'FP_{n} check failed'
    
    # Check: y_n^2 = 4n - 1
    assert y_n_sq == 4*n - 1, f'y^2 check failed at n={n}'
    
    # OP_n^2 = x_n^2 + y_n^2
    OP_sq = x_n**2 + y_n_sq
    total += OP_sq

print('Sum =', total)
if total == 882:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
