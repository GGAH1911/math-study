"""2019 고3 10월모의고사 나형 29번 — 파라미터 솔버 (수동).
첫째항 짝수. a_n 홀수→a_{n+1}=a_n+3, a_n 짝수→a_{n+1}=a_n/2. a_5=5일 때 가능한 첫째항 합.
역추적(BFS): 5←10←{20,7}←{40,17,14}←a_1 짝수 {80,34,28}. 합=142. (답 142)"""
def preimages(v):
    res=[]
    if v*2 % 1==0: res.append(v*2)            # 짝수였다면 a_n/2=v → a_n=2v (항상 짝수, 유효)
    if (v-3)>0 and (v-3)%2==1: res.append(v-3) # 홀수였다면 a_n+3=v → a_n=v-3 (홀수여야)
    return res
def solve(a5=5, steps=4):
    layer={a5}
    for _ in range(steps):
        nxt=set()
        for v in layer:
            for p in preimages(v): nxt.add(p)
        layer=nxt
    return sum(a for a in layer if a%2==0)       # 첫째항 짝수
assert solve()==142, solve()
print('VERIFY_PASS')
