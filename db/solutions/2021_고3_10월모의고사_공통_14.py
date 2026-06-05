from fractions import Fraction

# 검증: 답이 정말 7인지 확인
def f(n):
    return Fraction(3, 2) ** (n - 1)

def g(n):
    return 2 * (Fraction(3, 2) ** (n - 1)) - 2

p = Fraction(1, 2)
result = f(6 * p) + g(8 * p)
result_simplified = f(3) + g(4)

print(f'p = {p}')
print(f'6p = {6*p}, 8p = {8*p}')
print(f'f(3) = {f(3)}')
print(f'g(4) = {g(4)}')
print(f'f(3) + g(4) = {result_simplified}')
print(f'답: {int(result_simplified)}')

if result_simplified == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')