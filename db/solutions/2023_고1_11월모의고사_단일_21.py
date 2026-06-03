from itertools import product as iprod

def verify():
    valid = []
    for vals in iprod(range(6), repeat=8):
        a,b,c,d,e,f,g,h = vals
        if a+b+c+d+e+f+g+h != 5:
            continue
        if a+e != 2: continue
        if e+f != 1: continue
        if e+g != 2: continue
        nA = a+b+c+d
        nB = a+b+e+f
        nC = a+c+e+g
        valid.append((a, nA, nB, nC))

    # ㄱ: n(A∩B∩C) ≠ 0 always
    gak = all(v[0] != 0 for v in valid)

    # ㄴ: if n(A∩B∩C)=2 then n(C)=4
    nal = all(v[3] == 4 for v in valid if v[0] == 2)

    # ㄷ: max+min of n(A)*n(B)*n(C) == 42
    prods = [v[1]*v[2]*v[3] for v in valid]
    deut = (max(prods) + min(prods) == 42)

    print(f'n cases={len(valid)}, products min={min(prods)} max={max(prods)} sum={min(prods)+max(prods)}')
    print(f'gak={gak}, nal={nal}, deut={deut}')
    if gak and nal and deut:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()
