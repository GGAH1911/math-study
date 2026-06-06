import sympy as sp
from sympy import symbols, solve

# 주어진 값
a1 = 3
d = 6

# 등차수열 n번째 항
def a_n(n):
    return a1 + (n-1)*d

# 조건 (나) 검증: k=5일 때 a2, a5, a14가 등비수열
k = 5
a2 = a_n(2)
a5 = a_n(5)
a14 = a_n(14)

# 등비수열 조건: a5^2 = a2 * a14
geo_check = (a5**2 == a2 * a14)

# 조건 (가) 검증: a1 <= d
cond_ga = (a1 <= d)

# 범위 조건: 90 <= a16 <= 100
a16 = a_n(16)
range_check = (90 <= a16 <= 100)

# 최종 답: a20
a20 = a_n(20)

if geo_check and cond_ga and range_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')