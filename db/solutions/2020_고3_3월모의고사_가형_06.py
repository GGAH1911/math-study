import sympy as sp
n = sp.Symbol('n')
f = n**2 - 9*n + 18

# 부등식 조건
cond1 = sp.solve(f < 18, n)
cond2 = sp.solve(f > 0, n)

print('n^2 - 9n + 18 < 18:', cond1)
print('n^2 - 9n + 18 > 0:', cond2)

# 교집합 구하기
natural_nums = []
for i in range(1, 10):
    val = f.subs(n, i)
    if val > 0 and val < 18:
        natural_nums.append(i)

print('조건 만족 자연수:', natural_nums)
print('합:', sum(natural_nums))

if sum(natural_nums) == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')