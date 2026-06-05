import math
a = 1/2
f_pi = math.sin(a * math.pi + math.pi/6)
print(f'f(π) = {f_pi}')
print(f'√3/2 = {math.sqrt(3)/2}')
if abs(f_pi - math.sqrt(3)/2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')