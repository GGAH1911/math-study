from fractions import Fraction

# A의 속력: 150 m/min
v_A = 150

# 조건 1: 반대 방향 1.5분 후 만남
# (v_A + v_B) * 1.5 = 400
v_B = (400 / 1.5) - v_A

# 조건 2 검증: (v_A - v_B) * 12 = 400
condition2 = (v_A - v_B) * 12

# A의 한 바퀴 시간 (초)
time_A_seconds = (400 / v_A) * 60
minutes = int(time_A_seconds // 60)
seconds = int(time_A_seconds % 60)

if abs(condition2 - 400) < 0.001 and minutes == 2 and seconds == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')