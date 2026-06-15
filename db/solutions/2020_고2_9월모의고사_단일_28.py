# (1/4)^x-(3n+16)(1/2)^x+48n<=0 ⟺ (y-3n)(y-16)<=0 (y=(1/2)^x). 정수 x 개수=2 인 자연수 n 개수?
CANDIDATE = 12
cnt_n = 0
for n in range(1, 60):
    lo, hi = min(3*n, 16), max(3*n, 16)
    c = sum(1 for x in range(-40, 12) if lo - 1e-9 <= (0.5)**x <= hi + 1e-9)
    if c == 2:
        cnt_n += 1
print('VERIFY_PASS' if cnt_n == CANDIDATE else 'VERIFY_FAIL')
