# A={√a 자연수}={1..⌊√k⌋}, B={log_√3 b 자연수}={2m:3^m<=k}. C=A∩B 자연수.
# x=2m∈C ⟺ 4m²<=k & 3^m<=k. n(C)=3 인 자연수 k 의 개수?
CANDIDATE = 45
def nC(k): return sum(1 for m in range(1, 20) if k >= max(4*m*m, 3**m))
print('VERIFY_PASS' if sum(1 for k in range(1, 300) if nC(k) == 3) == CANDIDATE else 'VERIFY_FAIL')
