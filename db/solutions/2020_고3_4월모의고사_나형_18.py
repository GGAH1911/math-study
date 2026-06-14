import sympy as sp

# 공통밑 a>0, a!=1. 세 조건을 a의 거듭제곱 관계로 그대로 옮겨 검사한다.
a = sp.Symbol('a', positive=True)

count = 0
pairs = []
# c^4=a^12 이면 mn=18 이 강제되고 m,n>=2 이므로 둘 다 <=9. 25는 충분히 넉넉한 상한.
for m in range(2, 25):        # m: 1이 아닌 자연수
    for n in range(2, 25):    # n: 1이 아닌 자연수
        # (가) cube_root(a) 가 b의 m제곱근:  (a**(1/3))**m = b
        b = (a**sp.Rational(1, 3))**m
        # (나) sqrt(b) 가 c의 n제곱근:        (b**(1/2))**n = c
        c = (b**sp.Rational(1, 2))**n
        # (다) c 가 a**12 의 네제곱근:        c**4 = a**12
        ratio = sp.simplify((c**4) / (a**12))   # a!=1 이면 지수가 0일 때만 정확히 1
        if ratio == 1:
            # a,b,c != 1: a!=1 가정, b,c 는 a 의 양의 지수승이므로 자동 만족
            count += 1
            pairs.append((m, n))

print('valid (m,n):', pairs)
print('count =', count)
print('VERIFY_PASS' if count == 4 else 'VERIFY_FAIL')
