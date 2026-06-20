import sympy as sp
# a_{2n}=a2*a_n+1, a_{2n+1}=a2*a_n-2, 0<a1<1, a7=2 → a25?  (공식정답 82=③)
# a2 는 n=1 에서 a2=a2*a1+1 → a2=1/(1-a1). a3=a2*a1-2, a7=a2*a3-2=2 로 a1 결정.
t = sp.symbols('t')
b = 1/(1 - t)                                    # a2
a3 = b*t - 2                                      # a_3 = a2*a1 - 2
a7 = b*a3 - 2                                      # a_7 = a2*a3 - 2
sols = [s for s in sp.solve(sp.Eq(a7, 2), t) if s.is_real and 0 < s < 1]
assert len(sols) == 1, sols
a1 = sols[0]                                       # 3/4
a2 = 1/(1 - a1)                                    # 4
A = {1: a1, 2: a2}
def a(n):
    if n in A:
        return A[n]
    A[n] = a2*a(n//2) + 1 if n % 2 == 0 else a2*a((n-1)//2) - 2
    return A[n]
assert sp.nsimplify(a(7)) == 2
res = sp.nsimplify(a(25))
print('VERIFY_PASS' if res == 82 else f'VERIFY_FAIL {res}')
