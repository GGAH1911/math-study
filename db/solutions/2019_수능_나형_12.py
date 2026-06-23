import math

# Given values
sigma = 1.4
n = 49
z_alpha_2 = 1.96
upper_limit = 7.992

# Calculate standard error
SE = sigma / math.sqrt(n)
print(f'SE = {SE}')

# Calculate margin of error
E = z_alpha_2 * SE
print(f'Margin of Error = {E}')

# Calculate sample mean from upper limit
sample_mean = upper_limit - E
print(f'Sample Mean = {sample_mean}')

# Calculate a (lower limit)
a = sample_mean - E
print(f'a = {a}')

# Verify: the confidence interval should be [a, upper_limit]
lower_limit = a
print(f'\nConfidence Interval: [{lower_limit}, {upper_limit}]')
print(f'Center: {(lower_limit + upper_limit)/2}')

if abs(a - 7.208) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')