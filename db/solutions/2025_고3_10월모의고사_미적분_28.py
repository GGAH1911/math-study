from sympy import *
x = symbols('x', real=True)
q_val = Rational(7, 16)
p_val = Integer(0)
f = (x - p_val)**2 + q_val
r = sqrt(1 - q_val)  # = 3/4
a1, a2, a3 = -r, Integer(0), r
# g(x) = f(x)*ln(f(x)) - f(x) + 1  (from f(k)=1 condition)
g = f*ln(f) - f + 1
# Check critical points of g
f_prime = diff(f, x)
g_prime = f_prime * ln(f)
crit_ok = (simplify(g_prime.subs(x, a1)) == 0 and
           simplify(g_prime.subs(x, a2)) == 0 and
           simplify(g_prime.subs(x, a3)) == 0)
# Check condition (가): g >= 0, minimum = 0 at a1, a3
cond_ga_1 = simplify(g.subs(x, a1)) == 0
cond_ga_3 = simplify(g.subs(x, a3)) == 0
# Check integrand = 1
integrand = simplify(g + f - f*ln(f))
cond_integrand = (integrand == 1)
# Check condition (나)
integral_val = integrate(integrand, (x, a1, a3))
cond_na = simplify(integral_val - Rational(3, 2)) == 0
# Check f(a2)
f_a2 = f.subs(x, a2)
cond_ans = (f_a2 == Rational(7, 16))
if all([crit_ok, cond_ga_1, cond_ga_3, cond_integrand, cond_na, cond_ans]):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: crit={crit_ok}, ga1={cond_ga_1}, ga3={cond_ga_3}, intgd={cond_integrand}, na={cond_na}, ans={cond_ans}')