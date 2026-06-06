from math import comb, factorial

# Step 1: Choose 5 people including A, B from 8 people
choose_5 = comb(6, 3)  # A, B fixed, choose 3 from remaining 6

# Step 2: A and B sit adjacently
# Treat (AB) as one unit, so we have 4 units to arrange in a circle
arrangements_circle = factorial(3)  # (4-1)! for circular arrangement
ab_order = factorial(2)  # A-B or B-A
adjacentcases = arrangements_circle * ab_order

# Total cases where A and B are adjacent
total = choose_5 * adjacentcases

if total == 240:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')