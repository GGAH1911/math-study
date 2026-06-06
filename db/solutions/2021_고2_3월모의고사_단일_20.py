# 조건 검증
# f(1)=5, f(2)=3, f(3)=2, f(4)=4 (조건을 만족하는 경우)
f = {1: 5, 2: 3, 3: 2, 4: 4}
g = {2: f[2]+1, 3: f[3]+1, 4: f[4]+1, 5: None}  # g(5)는 미정

# 보기 그 검증: g∘f의 치역이 Z인가?
composition_image = set()
for x in [1, 2, 3, 4]:
    if x in [2, 3, 4]:  # x ∈ X∩Y
        composition_image.add(f[x] + 1)
    else:  # x=1
        if g[5] is not None:
            composition_image.add(g[5])

# f(2)=3, f(3)=2, f(4)=4이므로 {4, 3, 5}는 항상 포함
image_without_g5 = {f[2]+1, f[3]+1, f[4]+1}
print(f'f(2)+1={f[2]+1}, f(3)+1={f[3]+1}, f(4)+1={f[4]+1}')
print(f'치역의 부분 = {image_without_g5}')
print(f'Z = {{3, 4, 5}}')
if image_without_g5 == {3, 4, 5}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')