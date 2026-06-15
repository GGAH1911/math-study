import numpy as np
# f(x)=sinx-1/2 (0<=x<a), k sinx-1/2 (a<=x<=2π). (가)max|f|=1/2 (나)f=0 근 3개.
# → a=π, k=-1/2. |f|=1/4 근합 S. 20((a+S)/π+k)?
CANDIDATE = 110
a, k = np.pi, -0.5
def f(x):
    return np.sin(x) - 0.5 if x < a else k*np.sin(x) - 0.5
xs = np.linspace(0, 2*np.pi, 4000001)
fv = np.array([f(x) for x in xs])
ga = abs(np.max(np.abs(fv)) - 0.5) < 1e-3                       # (가) max|f|=1/2
na = all(abs(f(r)) < 1e-9 for r in [np.pi/6, 5*np.pi/6, 3*np.pi/2])  # (나) 3근
# S: |f(x)|=1/4 근들의 합 (모두 횡단교차)
g = np.abs(fv) - 0.25
sc = np.where(np.diff(np.sign(g)) != 0)[0]
S = sum((xs[i]+xs[i+1])/2 for i in sc)
val = 20*((a + S)/np.pi + k)
print('VERIFY_PASS' if ga and na and abs(val - CANDIDATE) < 0.2 else 'VERIFY_FAIL')
