"""2019 고3 10월모의고사 나형 12번 — 파라미터 솔버 (수동).
이차 f(아래로 볼록), 꼭짓점 x=2(f'(2)=0), y=2 와 x=-3,7 서 교차(그림). 열린구간 (-3,7)서
f'(x){f(x)-2}≤0 인 정수 개수. (답 ② 5)
f'(f-2)=½(d/dx)(f-2)² ≤0 ⟺ (f-2)² 비증가 = (-∞,-3]∪[2,7]. (-3,7) 정수 {2,3,4,5,6} → 5."""
def solve(vertex=2, clo=-3, chi=7, lo=-3, hi=7):
    cnt=0
    for x in range(lo+1, hi):                  # 열린구간 정수
        fp = vertex - x                         # f' 부호(아래볼록): x<vertex면 +
        fm = (x-clo)*(chi-x)                     # f-2 부호: 교차 사이서 +
        if fp*fm <= 0: cnt+=1
    return cnt
assert solve()==5, solve()
print('VERIFY_PASS')
