import math

# 검증: a_n = (1/n) * log2((n+1)/n)
# 따라서 n*a_n = log2((n+1)/n)

# f(8) = 8 + 1 = 9
f_8 = 9

# g(8) = log2(9/8)
g_8 = math.log2(9) - math.log2(8)

# h(8) = log2(9)
h_8 = math.log2(9)

result = f_8 - g_8 + h_8

print(f'f(8) = {f_8}')
print(f'g(8) = log2(9/8) = {g_8}')
print(f'h(8) = log2(9) = {h_8}')
print(f'f(8) - g(8) + h(8) = {result}')
print(f'Rounded result = {round(result)}')

if abs(round(result) - 12) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')