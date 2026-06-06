# k=10에서 조건 검증
k = 10

# 집합 정의
U = set(range(1, k+1))
A = {x for x in U if x % 2 == 0}
B = {x for x in U if k % x == 0}

# (A ∪ B)^C 구하기
A_union_B = A | B
complement = U - A_union_B

# 조건 검증
product_n = len(A) * len(complement)
print(f'n(A) = {len(A)}')
print(f'n((A∪B)^C) = {len(complement)}')
print(f'n(A) × n((A∪B)^C) = {product_n}')
print(f'조건 n(A) × n((A∪B)^C) = 15 만족: {product_n == 15}')

# 답 검증
result = 1
for elem in complement:
    result *= elem
print(f'(A∪B)^C의 원소: {sorted(complement)}')
print(f'모든 원소의 곱: {result}')
print(f'{result} == 189: {result == 189}')

if product_n == 15 and result == 189:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')