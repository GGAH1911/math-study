from sympy import symbols, solve

# 최댓값을 주는 경우: a_1=6, a_2=3, a_3=6, a_4=12
a1, a2, a3, a4 = 6, 3, 6, 12

# 조건 (가) 확인: a_1 = a_3
assert a1 == a3, f"조건 (가) 위반: {a1} != {a3}"

# 조건 (나) 확인
# n=1: (a_2 - a_1 + 3)(a_2 - 2*a_1) = 0
check1 = (a2 - a1 + 3) * (a2 - 2*a1)
assert check1 == 0, f"n=1 조건 위반: {check1} != 0"

# n=2: (a_3 - a_2 + 3)(a_3 - 2*a_2) = 0
check2 = (a3 - a2 + 3) * (a3 - 2*a2)
assert check2 == 0, f"n=2 조건 위반: {check2} != 0"

# n=3: (a_4 - a_3 + 3)(a_4 - 2*a_3) = 0
check3 = (a4 - a3 + 3) * (a4 - 2*a3)
assert check3 == 0, f"n=3 조건 위반: {check3} != 0"

print('VERIFY_PASS')