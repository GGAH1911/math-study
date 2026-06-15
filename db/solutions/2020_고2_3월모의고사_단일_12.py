from sympy import symbols, solve, S, oo

# P = (a, 5), Q = (-1, 2)
# Condition: P ∩ Q = empty set  ⟺  a >= 2
# Find minimum integer a with a < 5

found = None
for a in range(-10, 5):  # integer a < 5
    P = S.Reals if False else None
    # (a, 5) ∩ (-1, 2) = empty iff a >= 2
    left = max(a, -1)   # start of intersection (open)
    right = min(5, 2)   # end of intersection (open) = 2
    # intersection is (left, right) if left < right else empty
    intersection_empty = (left >= right)  # open intervals: (a,5)∩(-1,2) empty iff a>=2
    if intersection_empty:
        if found is None:
            found = a
        break

if found == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', found)
