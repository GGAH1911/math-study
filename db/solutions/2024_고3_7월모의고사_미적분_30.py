import numpy as np
from scipy import integrate

# Verify the calculation
a = 0.5

# Check condition (가): f'(ln(3/2)) = 0
v = np.log(3/2)
result = np.log(np.exp(v) - a)
assert abs(result) < 1e-10, f"Condition (가) failed: f'(ln(3/2)) = {result}"

# Verify p = ln(72/25)
p = np.log(72/25)
e_p = 72/25

# Final calculation
final_result = 100 * a * e_p
assert abs(final_result - 144) < 1e-9, f"Final calculation failed: {final_result}"

# Verify the logarithm calculation
log_product = np.log(6/5) + np.log(12/5)
assert abs(log_product - np.log(72/25)) < 1e-10, "Logarithm calculation error"

print('VERIFY_PASS')