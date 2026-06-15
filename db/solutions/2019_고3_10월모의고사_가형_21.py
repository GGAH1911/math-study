"""2019 고3 10월모의고사 가형 21번 — 파라미터 솔버 (수동).
점 (a,0)에서 y=(x-n)e^x 에 그은 접선 개수 f(n). 접점 t: 0-(t-n)e^t=(t-n+1)e^t(a-t)
→ t²-(a+n)t+(na+n-a)=0. 판별식 D=(a-n)(a-n+4). f=2(D>0)/1(D=0)/0(D<0).
ㄱ:a=0,f(4)=1✓  ㄴ:f(n)=1 정수 n은 항상 {a,a+4} 2개라 거짓  ㄷ:Σ₁⁵f=5 ↔ a∈{-1,3}✓ → ③ ㄱ,ㄷ."""
def f(a,n):
    D=(a-n)*(a-n+4)
    return 2 if D>0 else (1 if D==0 else 0)
g  = f(0,4)==1
nu = any(sum(1 for n in range(a-12,a+13) if f(a,n)==1)==1 for a in range(-60,61))
da = set(a for a in range(-60,61) if sum(f(a,n) for n in range(1,6))==5)=={-1,3}
choice={(1,0,1):3,(1,1,0):2,(1,0,0):1,(0,1,1):4,(1,1,1):5}
assert choice[(int(g),int(nu),int(da))]==3
print('VERIFY_PASS')
