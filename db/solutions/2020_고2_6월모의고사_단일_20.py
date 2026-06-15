import math
import sympy as sp

# ㄴ: AC=1 => a=2
# AC=1 iff log_{a+2}(a)=1/2 iff sqrt(a+2)=a iff a^2-a-2=0
a = sp.Symbol('a')
sols = sp.solve(a**2 - a - 2, a)  # [-1, 2]
valid = [float(s) for s in sols if float(s) > 1]
nieun_pass = (len(valid) == 1 and abs(valid[0] - 2.0) < 1e-10)

# Also directly verify: when a=2, AC should equal 1
a_val = 2.0
C_y_check = 2 * math.log(a_val) / math.log(a_val + 2)
AC_direct = 2 - C_y_check  # 2 - 2*log_4(2) = 2 - 1 = 1
nieun_pass = nieun_pass and abs(AC_direct - 1.0) < 1e-10

# ㄷ: S2/S1 = log_a(a+2) for all a>1
# h1 = 2 - C_y, h2 = D_y - 2, ratio = h2/h1
digeut_pass = True
for a_val in [1.5, 2.0, 3.0, 5.0, 10.0, 50.0]:
    C_y = 2 * math.log(a_val) / math.log(a_val + 2)
    D_y = 2 * math.log(a_val + 2) / math.log(a_val)
    h1 = 2 - C_y   # positive since log_{a+2}(a) < 1
    h2 = D_y - 2   # positive since log_a(a+2) > 1
    ratio = h2 / h1
    expected = math.log(a_val + 2) / math.log(a_val)  # log_a(a+2)
    if abs(ratio - expected) > 1e-9:
        digeut_pass = False
        break

# ㄱ is trivially true: log_a(a^2)=2 by definition
giyok_pass = True

if giyok_pass and nieun_pass and digeut_pass:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: ㄱ={giyok_pass}, ㄴ={nieun_pass}, ㄷ={digeut_pass}')
