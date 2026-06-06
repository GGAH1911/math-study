"""
2021 6월모평 가형 30번
주기함수의 불연속점과 극한값의 합

f(x) = |x-1| + |x-2| (0≤x<3), 주기 3
g(x)의 불연속점: f'+(2^x)의 점프점
  → 2^x = 3k+1 (Type A): g(a)=0
  → 2^x = 3k+2 (Type B): g(a)=2(3k+2)ln2

x∈(-5,5) ⟺ 2^x∈(1/32, 32)
  Type A: k=0~10 (11개), Type B: k=0~9 (10개)
  합 = n + Σg(a_k)/ln2 = 21 + 2×(2+5+8+...+29) = 21 + 310 = 331
"""

def solve():
    # Type A: 2^a = 3k+1, k=0~10
    # Type B: 2^b = 3k+2, k=0~9

    # 불연속점 개수
    n = 11 + 10  # Type A 11개 + Type B 10개 = 21

    # Type B에서의 합 계산
    # Σ(k=0 to 9) 2(3k+2) = 2×Σ(3k+2)
    type_b_sum = sum(2 * (3*k + 2) for k in range(10))

    result = n + type_b_sum

    return result

if __name__ == '__main__':
    answer = solve()
    print(f"답: {answer}")
