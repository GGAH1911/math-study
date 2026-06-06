import sympy as sp
x = sp.Symbol('x')
result = True

# 수열 정의
a = [4, 3, 2, 1, -3, -1, -1, -3, 1, 2]

# 조건 (가) 검증: 각 a[k-1]이 해당 방정식의 근인지 확인
for k in range(1, 11):
    eq = x**2 + 3*x + (8-k)*(k-5)
    val = eq.subs(x, a[k-1])
    if not sp.simplify(val) == 0:
        result = False
        break

# 조건 (나) 검증: aₙ × aₙ₊₁ ≤ 0인 n의 개수가 정확히 2
count = 0
for n in range(9):
    if a[n] * a[n+1] <= 0:
        count += 1

if count != 2:
    result = False

if result:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')