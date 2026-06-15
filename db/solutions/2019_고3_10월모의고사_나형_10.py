from sympy import symbols, Rational

def a(n):
    total = 0
    # line x=n, region S: 2x-y>=0 and y>0, integer y
    y = 1
    while True:
        # constraints: y>0 (y>=1) and 2*n - y >= 0  => y <= 2n
        if 2*n - y >= 0:
            total += n + y  # sum of x-coord and y-coord of point (n,y)
            y += 1
        else:
            break
    return total

# closed form check
def a_closed(n):
    return 4*n**2 + n

assert all(a(n) == a_closed(n) for n in range(1, 30)), 'count/sum mismatch'

val = a(10) - a(5)
CANDIDATE = 305
print('a10=', a(10), 'a5=', a(5), 'diff=', val)
if val == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
