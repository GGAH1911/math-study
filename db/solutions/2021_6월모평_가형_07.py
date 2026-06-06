from fractions import Fraction
def f(k):
    r=Fraction(k,4)
    if abs(r)<1: return Fraction(-1,3)
    if r==1: return Fraction(2*1-1,1+3)
    if r==-1: return Fraction(-2-1,4)
    return 2*r
cnt=[k for k in range(-1000,1001) if f(k)==Fraction(-1,3)]
print('VERIFY_PASS' if len(cnt)==7 else 'VERIFY_FAIL')