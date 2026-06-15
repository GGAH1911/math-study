from sympy import symbols, Eq, solve, Rational, nsimplify

pA, pB = symbols('pA pB', positive=True)

# Independence: P(A|B) = P(A) = 1/3
eq1 = Eq(pA, Rational(1,3))
# Independence of A and B^C: P(A and B^C) = P(A)*(1-P(B)) = 1/12
eq2 = Eq(pA*(1-pB), Rational(1,12))

sol = solve([eq1, eq2], [pA, pB], dict=True)[0]
pA_val = sol[pA]
pB_val = sol[pB]

# Check all original conditions
cond_indep_cond = (pA_val == Rational(1,3))           # P(A|B)=P(A)=1/3
cond_inter = (pA_val*(1-pB_val) == Rational(1,12))    # P(A∩B^C)=1/12
valid_prob = (0 <= pB_val <= 1) and (0 <= pA_val <= 1)

if cond_indep_cond and cond_inter and valid_prob and pB_val == Rational(3,4):
    print('P(B) =', pB_val)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
