import math

result = 'VERIFY_PASS'
total = 0

for a in [8, 27, 64]:
    b = a ** (3/2)
    c = a ** (-1/6)
    
    # 원래 조건 검증: -4*log_a(b) = 54*log_b(c) = log_c(a)
    term1 = -4 * math.log(b) / math.log(a)
    term2 = 54 * math.log(c) / math.log(b)
    term3 = math.log(a) / math.log(c)
    
    if not (abs(term1 - term2) < 1e-9 and abs(term2 - term3) < 1e-9):
        result = 'VERIFY_FAIL'
        break
    
    bc = b * c
    if bc > 300 or abs(bc - round(bc)) > 1e-9:
        result = 'VERIFY_FAIL'
        break
    
    total += a

if total == 99:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')