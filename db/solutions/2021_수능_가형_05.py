import math

# 부등식: (1/9)^x < 3^(21-4x)
# 이를 3^(-2x) < 3^(21-4x)로 정리

# 답: x = 1부터 10까지 만족하는지 확인
count = 0
for x in range(1, 15):
    lhs = (1/9) ** x
    rhs = 3 ** (21 - 4*x)
    if lhs < rhs:
        count += 1
        print(f"x={x}: {lhs} < {rhs} ✓")
    else:
        print(f"x={x}: {lhs} < {rhs} ✗")

print(f"\n자연수 x의 개수: {count}")
if count == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')