import sympy as sp
# a_{2n}=b_n+2, a_{2n+1}=b_n-1, b_{2n}=3a_n-2, b_{2n+1}=-a_n+3.
# a48=9, Σ_{1}^{63}a - Σ_{1}^{31}b = 155. b32?
CANDIDATE = 79
a1, b1 = sp.symbols('a1 b1')
A, B = {1: a1}, {1: b1}
def ga(n):
    if n not in A:
        A[n] = gb(n//2)+2 if n % 2 == 0 else gb((n-1)//2)-1
    return A[n]
def gb(n):
    if n not in B:
        B[n] = 3*ga(n//2)-2 if n % 2 == 0 else -ga((n-1)//2)+3
    return B[n]
sol = sp.solve([sp.Eq(ga(48), 9),
                sp.Eq(sum(ga(n) for n in range(1, 64)) - sum(gb(n) for n in range(1, 32)), 155)],
               [a1, b1])
print('VERIFY_PASS' if gb(32).subs(sol) == CANDIDATE else 'VERIFY_FAIL')
