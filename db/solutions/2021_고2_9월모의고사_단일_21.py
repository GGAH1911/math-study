def verify():
    def S(b, n):
        return n * (b - 2*n + 2)
    
    def check(b, N=500):
        return all(abs(S(b, n)) >= 14 for n in range(1, N+1))
    
    valid = [b for b in range(1, 300) if check(b)]
    
    expected = [27 + 2*i for i in range(10)]
    total = sum(valid[:10])
    
    if valid[:10] == expected and total == 360:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: valid[:10]={valid[:10]}, sum={total}')

verify()