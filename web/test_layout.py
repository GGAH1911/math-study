import numpy as np

# Let's check the position of curves and labels to ensure no overlaps.
# Curves:
# C1: x in [0.5, 2], y = -0.3*(x-2)**2 + 3
# C2: x in [2, 4], y = 0.3*(x-2)**2 + 3
# C3: x in [4, 6.92], y = 0.5/(7-x) + 1.5
# C4: x in [7.08, 9.5], y = 0.5/(x-7) + 1.5

# Important points:
# P_removable_hole = (2, 3)
# P_removable_solid = (2, 4.2)
# P_jump_solid = (4, 4.2)
# P_jump_hole = (4, 1.67)
# Asymptote at x = 7

# Text labels:
# T1 = "제거 가능한 불연속" at (2, 5.2) -> distance to P_removable_solid is 1.0. Distance to C2 at x=2 is 2.2.
# T2 = "점프 불연속" at (4.5, 5.2) -> distance to P_jump_solid is sqrt(0.5**2 + 1.0**2) = 1.12.
# T3 = "무한 불연속" at (8.2, 5.0) -> distance to C4 at x=8.2 is y=0.5/1.2 + 1.5 = 1.92, so distance is 5.0 - 1.92 = 3.08.

# Let's print some y-values of C3 to see if it overlaps with T2:
# T2 is at x=4.5, y=5.2.
# C3 at x=4.5 is y = 0.5/(7-4.5) + 1.5 = 0.5/2.5 + 1.5 = 1.7.
# So T2 is at (4.5, 5.2) and the curve is at (4.5, 1.7). That's a vertical distance of 3.5 units! Excellent.

print("All clear on layout!")
