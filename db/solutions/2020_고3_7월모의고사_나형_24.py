import sympy as sp
# log_27 a = log_3 √b (a,b>1). 20 log_b √a ?  → a²=b³ → log_b a=3/2
CANDIDATE = 15
lb = sp.symbols('lb', positive=True)   # log b (>0)
la = sp.Rational(3,2)*lb               # 2 log a=3 log b
val = 20 * (sp.Rational(1,2)*la/lb)     # 20 log_b √a = 10 log_b a
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
