"""
2024 고2 10월모의고사 30번
함수의 연속성과 교점 개수 조건

g(x) = bx/(x+a) (x≠-a), f(x) (x≥1)
연속성: g(1-) = f(1)
h(t) = |g(x)|와 y=t의 교점 개수

Steps:
- c = b/(1+a) = f(1)
- h(0)=3, 불연속점 0, c, b
- h(0)=α ⟹ c=3
- h(α)=β-1 ⟹ 5=b-1 ⟹ b=6
- c=3 ⟹ a=1
- f(x)=(x-4)²-6
- f(a-b)=f(-5)=81-6=75
"""

def solve():
    # a=1, b=6에서
    # f(x) = (x-4)² - 6
    # f(a-b) = f(1-6) = f(-5)

    a = 1
    b = 6
    x_v = 4  # 꼭짓점 x좌표
    M = 6    # |f|의 최댓값

    # f(x) = (x - x_v)² - M
    target = a - b  # -5
    f_val = (target - x_v) ** 2 - M

    return f_val

if __name__ == '__main__':
    print(f"답: {solve()}")
