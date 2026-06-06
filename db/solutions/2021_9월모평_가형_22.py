"""
2021 9월모평 가형 22번
이항정리: (x + 4/x²)⁶ 전개에서 x³의 계수

일반항: C(6,k) × 4^k × x^(6-3k)
x³ 항의 조건: 6-3k = 3 → k=1
계수: C(6,1) × 4¹ = 6 × 4 = 24
"""

from math import comb

def solve():
    # (x + 4/x²)⁶ 전개
    # 일반항: C(6,k) × x^(6-k) × (4/x²)^k = C(6,k) × 4^k × x^(6-3k)

    # x³의 계수를 구하려면: 6 - 3k = 3
    # 3k = 3 → k = 1

    k = 1
    coeff = comb(6, k) * (4 ** k)

    return coeff

if __name__ == '__main__':
    answer = solve()
    print(f"답: {answer}")
