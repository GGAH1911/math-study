import math

log2_3 = math.log2(3)

# Case 1: a = 1 - log_2(3)
a1 = 1 - log2_3
f_max_1 = -2**(a1-1) + 2  # = -1/3 + 2 = 5/3
f_min_1 = -2**(a1+1) + 2  # = -4/3 + 2 = 2/3
diff_1 = f_max_1 - f_min_1  # = 1

# Case 2: a = 3
a2 = 3
f_min_2 = math.log2(a2-1)  # = log_2(2) = 1
f_max_2 = math.log2(a2+1)   # = log_2(4) = 2
diff_2 = f_max_2 - f_min_2  # = 1

# Case 3: a = 1
a3 = 1
f_0 = 1  # -2^0 + 2
f_1 = 0  # log_2(1)
f_2 = 1  # log_2(2)
max_f3 = max(f_0, f_2)
min_f3 = f_1
diff_3 = max_f3 - min_f3  # = 1

eps = 1e-10
if (abs(diff_1 - 1) < eps and 
    abs(diff_2 - 1) < eps and 
    abs(diff_3 - 1) < eps):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')