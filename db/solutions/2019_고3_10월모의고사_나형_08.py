from sympy import cbrt, sqrt, simplify, symbols, Eq, solve, N

# 후보 (m, n) 검사
candidates = [
    (108, 9),  # 최대값
    (108, 4),
    (108, 1),
    (32, 9),
    (32, 4),
    (32, 1),
    (4, 9),
    (4, 4),
    (4, 1)
]

max_sum = 0
for m, n in candidates:
    result = (2*m)**(1/3) * (n**3)**(1/2)
    # 자연수 확인
    if abs(result - round(result)) < 1e-9:
        total = m + n
        if total > max_sum:
            max_sum = total
            best_m, best_n = m, n

# 최종 검증: m=108, n=9
m, n = 108, 9
result = float((2*m)**(1/3) * (n**3)**(1/2))
if abs(result - round(result)) < 1e-9 and m <= 135 and n <= 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')