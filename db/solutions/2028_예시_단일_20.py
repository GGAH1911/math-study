A = -4; B = 4; C = -16
g_beta = A + B
h_beta = -A + B
h_gamma = -A + B + (-C)
assert abs(g_beta) < 1e-9, f'g(beta)={g_beta}'
assert abs(h_beta - 8) < 1e-9, f'h(beta)={h_beta}'
assert abs(h_gamma - 24) < 1e-9, f'h(gamma)={h_gamma}'
g_alpha = A
g_gamma = A + B + C
result = g_alpha - g_gamma
assert result == 12, f'result={result}'
print('VERIFY_PASS')