import numpy as np

def neg_p_holds(x, a):
    # ~p means (x-a)(x+2a) <= 0
    return (x - a) * (x + 2 * a) <= 0

def q_holds(x):
    return abs(x - 1) <= 5

def necessary_condition(a):
    # check that for all real x, ~p(x) implies q(x)
    # sample widely; root structure makes endpoints the binding case
    xs = np.linspace(-20, 20, 200001)
    np_mask = neg_p_holds(xs, a)
    q_mask = q_holds(xs)
    return bool(np.all(q_mask[np_mask]))

# Find numerical M and m by scanning a
as_grid = np.linspace(-10, 10, 2000001)
valid = np.array([necessary_condition(a) for a in np.linspace(-10, 10, 4001)])
as_coarse = np.linspace(-10, 10, 4001)
valid_as = as_coarse[valid]
M_num = float(valid_as.max())
m_num = float(valid_as.min())

# Compare with claimed answer
M_claim, m_claim = 2.0, -3.0
ans_claim = -1

# Tolerance
tol = 0.01

# Verify M, m
ok_M = abs(M_num - M_claim) < tol
ok_m = abs(m_num - m_claim) < tol

# Sanity: a=2 valid, a=2.01 invalid; a=-3 valid, a=-3.01 invalid
checks = [
    necessary_condition(2.0),
    not necessary_condition(2.05),
    necessary_condition(-3.0),
    not necessary_condition(-3.05),
    necessary_condition(0.0),
    necessary_condition(-1.5),
]

if ok_M and ok_m and all(checks) and (M_claim + m_claim) == ans_claim:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
