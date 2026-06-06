"""
2021 고1 3월모의고사 27번
이차함수 y=ax² 그래프 위 점과 도형의 넓이

A(-√(3/a), 3), B(√(3/a), 3), C(-1,-1), D(1,-1)
사다리꼴 ACDB의 넓이 = 4√(3/a) + 4

넓이가 자연수 ⟺ 4√(3/a) = k (k는 양의 정수)
a = 48/k²

a가 자연수 ⟺ k²|48 (48 = 2⁴×3)
k²의 약수: 1, 4, 16 (9는 48을 나누지 않음)
- k=1: a=48 ✓
- k=2: a=12 ✓
- k=4: a=3 ✓

최댓값: a=48
"""

from math import sqrt

def solve():
    # 넓이 = 4√(3/a) + 4가 자연수
    # 4√(3/a) ∈ ℤ ⟹ √(3/a) ∈ {0,1/4,1/2,3/4,1,...}
    # √(3/a) = k/4 (k는 양의 정수)
    # 3/a = k²/16
    # a = 48/k²

    # a가 자연수가 되려면 k²|48
    # 48 = 2⁴ × 3
    # k²의 가능한 값: 1, 4, 16

    candidates = []
    for k_squared in [1, 4, 9, 16, 25, 36]:
        if 48 % k_squared == 0:
            a = 48 // k_squared
            if a > 0:
                candidates.append(a)

    return max(candidates)

if __name__ == '__main__':
    answer = solve()
    print(f"답: {answer}")
