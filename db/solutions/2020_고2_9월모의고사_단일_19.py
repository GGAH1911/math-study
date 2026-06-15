import sympy as sp
# A=(log2 t,t),B=(1+log2 t,2t). f=□ABRP, g=□AQSB. f/g=(2log2 t+1)/3 자연수 인 t 의 곱? (③=2^13)
CANDIDATE = 2**13
ts = []
for m in range(1, 20):
    t = 2**sp.Rational(3*m-1, 2)                             # log2 t=(3m-1)/2
    if 1 < t < 100:
        ts.append(t)
prod = sp.prod(ts)
print('VERIFY_PASS' if sp.simplify(prod - CANDIDATE) == 0 else 'VERIFY_FAIL')
