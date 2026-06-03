import numpy as np

def get_a(k):
    return (3 - k) * (1 - 1.0/np.sqrt(k))

def f(x, k):
    return (x - k)**2

def g(x, k, a):
    if x <= 3:
        return f(x, k)
    else:
        return k * f(x - a, k)

k_values = np.linspace(1.01, 2.99, 500)

guk_pass = True
neun_pass = True
deut_always = True

for k in k_values:
    a = get_a(k)
    # a > 0 check
    if a <= 0:
        print('VERIFY_FAIL: a<=0'); exit()
    # (가) check
    left_lim = (3 - k)**2
    right_lim = k * (3 - a - k)**2
    if abs(left_lim - right_lim) > 1e-8:
        print('VERIFY_FAIL: (가) not satisfied'); exit()
    # (나) check: a+k < 3 → right piece no zero in x>3
    if a + k >= 3:
        print('VERIFY_FAIL: (나) violated'); exit()
    # guk: if f(1)==1 then g(2)==0
    if abs(f(1, k) - 1) < 1e-6:
        if abs(g(2, k, a)) > 1e-8:
            guk_pass = False
    # neun: g(k+a) < g(3)
    gka = g(k + a, k, a)
    g3 = g(3, k, a)
    if gka >= g3:
        neun_pass = False
    # deut: (k-1)(k-2) >= 0
    if (k - 1) * (k - 2) < 0:
        deut_always = False

# Answer 2 means guk=True, neun=True, deut=False
if guk_pass and neun_pass and not deut_always:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
