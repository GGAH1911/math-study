import sympy as sp
from sympy import sqrt, simplify

# 최종 답
answer = (3 + 2*sqrt(3)) / 12

# 검증: 선택지와의 일치 확인
opt1 = 3*sqrt(3) / 12
opt2 = (2 + sqrt(3)) / 6
opt3 = (3 + 2*sqrt(3)) / 12
opt4 = (2 + sqrt(3))/4
opt5 = (4 + sqrt(3))/6

print(f'검증: {simplify(answer - opt3) == 0}')
print(f'답: {answer}')
print(f'수치값: {float(answer):.6f}')

if simplify(answer - opt3) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')