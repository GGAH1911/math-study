import itertools
from math import gcd
from functools import reduce

# X = {-2, -1, 0, 2, 3, 4, 5}
X = {-2, -1, 0, 2, 3, 4, 5}

# Calculate A: all real fourth roots
A = set()
for x in X:
    if x > 0:
        fourth_root = x ** (1/4)
        A.add(fourth_root)
        A.add(-fourth_root)
    elif x == 0:
        A.add(0)

# Calculate B: all real cube roots  
B = set()
for x in X:
    cube_root = x ** (1/3) if x >= 0 else -abs(x) ** (1/3)
    B.add(cube_root)

# Verify conditions
print(f"n(A) = {len(A)}, expected 9")
print(f"n(B) = {len(B)}, expected 7")

# Verify sum
total = sum(X)
print(f"Sum of X = {total}")

if len(A) == 9 and len(B) == 7:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")