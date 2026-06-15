import sympy as sp

# 표에서 직접 읽은 값: log(3.24) = 0.5105
log324_table = sp.Rational(5105, 10000)

# log 32.4 = log(3.24*10) = log 3.24 + 1
result = log324_table + 1

# 실제 log10(32.4) 와 표 기반 근사가 소수 넷째 자리까지 일치하는지 확인
actual = sp.log(sp.Rational(324, 10), 10)
actual_num = float(actual)

# 표값 검증: log(3.24) 실제값이 0.5105로 반올림되는지
if round(float(sp.log(sp.Rational(324,100),10)), 4) == 0.5105 and abs(float(result) - actual_num) < 5e-4 and abs(float(result) - 1.5105) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
