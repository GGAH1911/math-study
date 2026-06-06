import sympy as sp
x, a = sp.symbols('x a')
b = 9
a_val = 12

# 조건 1: x - 1 > 8
cond1 = x - 1 > 8
# 조건 2: 2x - 16 <= x + a
cond2 = 2*x - 16 <= x + a_val

# 조건 1에서: x > 9
sol1 = sp.solve(x - 1 - 8, x)
print('x - 1 > 8 => x > 9')

# 조건 2에서: x <= a + 16 = 28
sol2 = sp.solve(2*x - 16 - (x + a_val), x)
print(f'2x - 16 <= x + {a_val} => x <= {a_val + 16}')

# x = 10일 때: 10 > 9 (참), 2(10) - 16 = 4 <= 10 + 12 = 22 (참)
test_val = 10
cond1_check = test_val - 1 > 8
cond2_check = 2*test_val - 16 <= test_val + a_val
print(f'x=10: cond1={cond1_check}, cond2={cond2_check}')

# x = 28일 때: 28 > 9 (참), 2(28) - 16 = 40 <= 28 + 12 = 40 (참)
test_val = 28
cond1_check = test_val - 1 > 8
cond2_check = 2*test_val - 16 <= test_val + a_val
print(f'x=28: cond1={cond1_check}, cond2={cond2_check}')

# 경계값 확인
if b + 0.1 > 9 and 2*(b+0.1) - 16 <= (b+0.1) + a_val and a_val + 16 == 28:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')