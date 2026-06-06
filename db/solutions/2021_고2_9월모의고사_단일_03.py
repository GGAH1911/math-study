import sympy as sp

T = 6 * sp.pi

# cos(x/3)의 주기가 T인지 확인
# cos((x+T)/3) = cos(x/3 + T/3)이 cos(x/3)과 같으려면
# T/3 = 2π이어야 함

period_shift = T / 3
expected_shift = 2 * sp.pi

if sp.simplify(period_shift - expected_shift) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')