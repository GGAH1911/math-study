import math
# y=tan(nx-π/2)=-cot(nx) 와 y=-x 교점(즉 cot(nx)=x) 의 x∈(-π,π) 개수 a_n. a_2+a_3?
# cot(nx) 는 점근선 x=kπ/n 사이 구간마다 +∞→-∞ 단조감소 → y=x 와 1교점. a_n = 구간 수.
CANDIDATE = 10
def a(n):
    asy = sorted({round(k*math.pi/n, 12) for k in range(-n, n+1)
                  if -math.pi-1e-9 <= k*math.pi/n <= math.pi+1e-9})
    return len(asy) - 1
print('VERIFY_PASS' if a(2)+a(3) == CANDIDATE else 'VERIFY_FAIL')
