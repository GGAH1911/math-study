import sympy as sp
import math

a, b = 27, 243

# 조건 (가): a < b < a^2
cond_ga = (a < b) and (b < a**2)

# 조건 (나): log_a(b) 는 유리수
log_ab = sp.log(b) / sp.log(a)
log_simplified = sp.nsimplify(log_ab, rational=False)
cond_na = log_simplified.is_rational

# log10(a) < 3/2
cond_log = math.log10(a) < 1.5

# a, b != 1 이고 자연수
cond_nat = (a >= 2) and (b >= 2) and isinstance(a, int) and isinstance(b, int)

# a + b == 270
cond_val = (a + b == 270)

if cond_ga and cond_na and cond_log and cond_nat and cond_val:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: ga={cond_ga}, na={cond_na}, log={cond_log}, nat={cond_nat}, val={cond_val}')
