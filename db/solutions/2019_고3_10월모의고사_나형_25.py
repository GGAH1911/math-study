"""2019 고3 10월모의고사 나형 25번 — 파라미터 솔버 (수동).
U={1..9}, A: m∈A면 m²·n² 끝자리 같은 n≠m(∈A) 존재. 공집합 아닌 A 개수. (답 15)
끝자리² 그룹: {1,9}{2,8}{3,7}{4,6}{5}. {5}는 짝 없어 불가. 각 쌍 all-or-nothing → 2^4-1=15."""
def solve(U=range(1,10)):
    from collections import defaultdict
    g=defaultdict(list)
    for m in U: g[(m*m)%10].append(m)
    # 각 그룹: 크기≥2면 전부-or-전무(1개만 넣으면 짝 필요), 크기1이면 절대 불가
    pairs=[v for v in g.values() if len(v)>=2]; singles=[v for v in g.values() if len(v)==1]
    # 전수검증
    import itertools
    elems=list(U); cnt=0
    for r in range(1,len(elems)+1):
        for A in itertools.combinations(elems,r):
            S=set(A); ok=True
            for m in A:
                if not any(n!=m and (n*n)%10==(m*m)%10 for n in S): ok=False; break
            if ok: cnt+=1
    return cnt
assert solve()==15, solve()
print('VERIFY_PASS')
