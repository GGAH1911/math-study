# 함수의 정의를 다이어그램으로부터 추출
# 화살표 추적: 왼쪽 → 오른쪽
f_mapping = {
    1: 1,  # 또는 다른 값
    2: 4,  # 왼쪽 2 → 오른쪽 4
    3: 3,
    4: 5,
    5: 2
}

# f^{-1}(4)를 확인: f(x) = 4인 x를 찾기
inverse_4 = None
for x, y in f_mapping.items():
    if y == 4:
        inverse_4 = x
        break

if inverse_4 == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')