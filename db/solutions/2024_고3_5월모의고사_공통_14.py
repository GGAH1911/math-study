from sympy import symbols, solve, simplify

x = symbols('x')
f = x**3 - x**2 + x/4

# f(4)를 계산
result = f.subs(x, 4)
print(f"f(4) = {result}")
assert result == 49, f"Expected 49, got {result}"

# 검증: f(k)=0, g(k)=0의 해가 정확히 2개인지 확인
f_roots = solve(f, x)
print(f"f(x)=0의 해: {f_roots}")

f_prime = 3*x**2 - 2*x + 1/4
g = f - x*f_prime
g_simplified = simplify(g)
print(f"g(x) = {g_simplified}")

g_roots = solve(g_simplified, x)
print(f"g(x)=0의 해: {g_roots}")

# 공통 근
common_roots = set(f_roots) & set(g_roots)
print(f"f(k)=0 and g(k)=0의 공통 해: {common_roots}")
assert len(common_roots) == 2, f"Expected 2 common roots, got {len(common_roots)}"

# 조건 검증
f_1 = f.subs(x, 1)
g_1 = g_simplified.subs(x, 1)
check = 4*f_1 + 2*g_1
print(f"4f(1) + 2g(1) = {check}")
assert check == -1, f"Expected -1, got {check}"

print("VERIFY_PASS")