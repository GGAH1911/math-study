import sympy as sp

x, a, b = sp.symbols('x a b', real=True)
# f(x) = log2(x+a) + b ; inverse g(x): solve y = log2(x+a)+b for x with x<->y swapped
y = sp.symbols('y', real=True)
# from y = log(x+a,2)+b  -> x = 2**(y-b) - a ; so g(t) = 2**(t-b) - a
t = sp.symbols('t', real=True)
g = 2**(t - b) - a

# Condition 1: horizontal asymptote of g is y = 1 -> limit as t->-inf = -a = 1
asym = sp.limit(g, t, -sp.oo)  # = -a
eq1 = sp.Eq(asym, 1)

# Condition 2: g(3) = 2
eq2 = sp.Eq(g.subs(t, 3), 2)

sol = sp.solve([eq1, eq2], [a, b], dict=True)[0]
aval, bval = sol[a], sol[b]
ans = sp.simplify(aval + bval)

# re-check conditions hold with the original function
gg = g.subs(sol)
check_asym = sp.limit(gg, t, -sp.oo) == 1
check_pt = sp.simplify(gg.subs(t, 3) - 2) == 0
# also verify via original f: g passes (3,2) <=> f passes (2,3)
f = sp.log(x + aval, 2) + bval
check_f = sp.simplify(f.subs(x, 2) - 3) == 0

if check_asym and check_pt and check_f and ans == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
