"""
2025 고2 6월모의고사 단일 18번
지수·로그함수 대칭성과 직선으로 형성된 사각형의 넓이

키포인트:
- 지수함수와 로그함수는 y=x에 대해 대칭
- 기울기 -1인 직선은 대칭축 y=x-1/a에 수직
- 네 점 A, B, C, D는 기울기 -1인 직선으로 지그재그 연결
- 신발끈 공식으로 사각형 넓이 계산

풀이:
1. 점 C는 L의 x절편: C = (a+1/a, 0)
2. 대칭성으로부터 D = (1/a, a)
3. x_A - x_D = 1/a → x_A = 2/a → A = (2/a, a²)
4. 직선 AD 기울기 조건 → a = 2
5. a=2일 때: A(1,4), B(9/2,1/2), C(5/2,0), D(1/2,2)
6. 신발끈공식: 넓이 = 55/8 → 선택지 번호 5
"""

def solve():
    # a = 2로부터 결정됨
    a = 2

    # 네 점의 좌표
    A = (1, 4)
    B = (9/2, 1/2)
    C = (5/2, 0)
    D = (1/2, 2)

    # 신발끈 공식 (Shoelace formula)
    x_coords = [A[0], B[0], C[0], D[0]]
    y_coords = [A[1], B[1], C[1], D[1]]

    area = 0
    for i in range(len(x_coords)):
        j = (i + 1) % len(x_coords)
        area += x_coords[i] * y_coords[j]
        area -= x_coords[j] * y_coords[i]

    area = abs(area) / 2

    # 선택지 번호 (넓이가 55/8이므로 ⑤)
    return 5

if __name__ == '__main__':
    print(f"답: {solve()}")
