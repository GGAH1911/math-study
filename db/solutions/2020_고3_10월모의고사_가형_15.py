CANDIDATE='sqrt6/3'
import math
import sympy as sp
vals={'sqrt2/3':math.sqrt(2)/3,'sqrt3/3':math.sqrt(3)/3,'2/3':2/3,'sqrt5/3':math.sqrt(5)/3,'sqrt6/3':math.sqrt(6)/3}
a=vals[CANDIDATE]
# find p<0 with: R=P+(3.5,0.5), R on y=-log_a x, angle PQR=45
p=sp.symbols('p',real=True)
ok=False
for guess in [-2.0,-1.0,-3.0,-0.5,-4.0]:
    try:
        sol=sp.nsolve((a**p+sp.Rational(1,2)) + sp.log(p+sp.Rational(7,2))/sp.log(a), p, guess)
    except Exception:
        continue
    pv=float(sol)
    if pv>=0: continue
    q=a**pv
    P=(pv,q); Q=(q,pv); R=(pv+3.5,q+0.5)
    QP=(P[0]-Q[0],P[1]-Q[1]); QR=(R[0]-Q[0],R[1]-Q[1])
    nQP=math.hypot(*QP); nQR=math.hypot(*QR)
    cosang=(QP[0]*QR[0]+QP[1]*QR[1])/(nQP*nQR)
    PR=math.hypot(R[0]-P[0],R[1]-P[1])
    slope=(R[1]-P[1])/(R[0]-P[0])
    if (abs(cosang-math.cos(math.radians(45)))<1e-6 and abs(PR-5*math.sqrt(2)/2)<1e-9 and abs(slope-1/7)<1e-9):
        ok=True; break
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')