from sympy import symbols, solve, summation, simplify

n, x = symbols('n x')

# 이차방정식 계수
A = n**2 + 6*n + 5
B = -(n+5)
C = -1

# 비에타 공식으로 두 근의 합
a_n = -B / A
a_n_simplified = simplify(a_n)
print(f'a_n = {a_n_simplified}')

# 1/a_n 계산
inverse_a_n = simplify(1 / a_n_simplified)
print(f'1/a_n = {inverse_a_n}')

# k=1부터 10까지 합 계산
total = sum(k+1 for k in range(1, 11))
print(f'Sum = {total}')

if total == 65:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')