def f(x):
    if x < 0: return x + 1.0
    elif x < 1: return x - 1.0
    elif x <= 3: return 0.0
    else: return -x + 4.0

def fL(x):
    if x <= 0: return x + 1.0
    elif x <= 1: return x - 1.0
    elif x <= 3: return 0.0
    else: return -x + 4.0

def fR(x):
    if x < 0: return x + 1.0
    elif x < 1: return x - 1.0
    elif x < 3: return 0.0
    else: return -x + 4.0

def g(x, k): return abs(f(x - k))
def gL(x, k): return abs(fL(x - k))
def gR(x, k): return abs(fR(x - k))

# ㄱ
a1 = (gL(0, -3) == g(0, -3) == 0)

# ㄴ: 정수 k 존재하지 않아야 함
a2_exists = False
for k in range(-30, 31):
    L = fL(0) + gL(0, k)
    R = fR(0) + gR(0, k)
    V = f(0) + g(0, k)
    if abs(L - R) < 1e-9 and abs(R - V) < 1e-9:
        a2_exists = True
        break

# ㄷ: f*g 미분가능 정수 k 합 = -5
diff_ks = []
for k in range(-30, 31):
    Lp = fL(0) * gL(0, k)
    Rp = fR(0) * gR(0, k)
    Vp = f(0) * g(0, k)
    if not (abs(Lp - Rp) < 1e-9 and abs(Rp - Vp) < 1e-9):
        continue
    h = 1e-7
    Ld = (f(0)*g(0,k) - f(-h)*g(-h,k)) / h
    Rd = (f(h)*g(h,k) - f(0)*g(0,k)) / h
    if abs(Ld - Rd) < 1e-3:
        diff_ks.append(k)
a3 = (sum(diff_ks) == -5) and (set(diff_ks) == {1, -2, -4})

if a1 and (not a2_exists) and a3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')