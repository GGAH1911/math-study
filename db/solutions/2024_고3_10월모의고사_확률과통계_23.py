from math import factorial

# 4개 문자(a,a,b,b)를 나열하는 경우의 수
# 중복순열: n!/(n1! * n2!) 여기서 n=4, n1=2(a개수), n2=2(b개수)

result = factorial(4) // (factorial(2) * factorial(2))
print(f'계산 결과: {result}')

if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')