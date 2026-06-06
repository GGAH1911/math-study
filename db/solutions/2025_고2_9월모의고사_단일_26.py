import sympy as sp

# 매개변수 정의
a, r = sp.symbols('a r', real=True)

# 조건 1: a_2 = -54
eq1 = sp.Eq(a * r, -54)

# 조건 2: 6*S_1 + S_2 + S_4 = 0
S1 = a
S2 = a * (1 + r)
S4 = a * (1 + r + r**2 + r**3)
eq2 = sp.Eq(6*S1 + S2 + S4, 0)

# 연립 방정식 풀이
solutions = sp.solve([eq1, eq2], [a, r])

# 첫째항이 양수인 해 찾기
valid_solution = None
for sol in solutions:
    a_val, r_val = sol
    if a_val > 0:
        valid_solution = (a_val, r_val)
        break

a_val, r_val = valid_solution
print(f"a = {a_val}, r = {r_val}")

# a_5 계산
a5 = a_val * (r_val ** 4)
print(f"a_5 = {a5}")

# 검증: 원래 조건 확인
S1_check = a_val
S2_check = a_val * (1 + r_val)
S4_check = a_val * (1 + r_val + r_val**2 + r_val**3)
verify = 6*S1_check + S2_check + S4_check

print(f"6*S_1 + S_2 + S_4 = {verify}")
print(f"a_2 check: {a_val * r_val}")

if sp.simplify(verify) == 0 and a_val * r_val == -54:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")