from sympy import *

# f 함수 정의
def f(k):
    units = [3**i % 10 for i in range(1, 10)]
    return units[k-1]

# f 값 확인
f_values = {i: f(i) for i in range(1, 10)}

# A = {1, 3, 7} 검증
A = {1, 3, 7}

# 조건 (가)
X = {1, 2, 3, 4, 5, 6, 7, 8, 9}
assert A.issubset(X) and len(A) >= 2, "조건 (가) 위반"

# 조건 (나): f(A) ⊆ A 및 (f∘f)(a) = 7
for a in A:
    fa = f(a)
    assert fa in A, f"f({a})={fa} not in A"
    ffa = f(fa)
    assert ffa == 7, f"(f∘f)({a})={ffa} ≠ 7"

# 조건 (다): x < y이면 f(x) ≤ f(y)
A_sorted = sorted(list(A))
for i in range(len(A_sorted)):
    for j in range(i+1, len(A_sorted)):
        x, y = A_sorted[i], A_sorted[j]
        assert f(x) <= f(y), f"f({x})={f(x)} > f({y})={f(y)}"

print("VERIFY_PASS")