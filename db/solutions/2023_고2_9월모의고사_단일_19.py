from sympy import *

a, r = Rational(5,3), Integer(3)

# 각 항 정의
a1 = a
a2 = Rational(75,1)/(a*r**3)
a3 = a*r
a4 = Rational(75,1)/(a*r**2)
a5 = a*r**2
a6 = Rational(75,1)/(a*r)
a7 = a*r**3
a8 = Rational(75,1)/a

terms = [a1,a2,a3,a4,a5,a6,a7,a8]

# 조건 (가): a1,a3,a5,a7이 공비가 양수인 등비수열
geo = [a1,a3,a5,a7]
cond_ga = (geo[1]/geo[0] == geo[2]/geo[1] == geo[3]/geo[2]) and (geo[1]/geo[0] > 0)

# 조건 (나): a_n * a_{9-n} = 75
cond_na = all(terms[n-1]*terms[9-n-1] == 75 for n in range(1,9))

# 주어진 조건
cond_sum1 = (a1 + a2 == Rational(10,3))
cond_sum8 = (sum(terms) == Rational(400,3))

# 답 검증
answer = a3 + a8
cond_answer = (answer == 50)

if cond_ga and cond_na and cond_sum1 and cond_sum8 and cond_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'(가):{cond_ga}, (나):{cond_na}, sum1:{cond_sum1}, sum8:{cond_sum8}, ans:{cond_answer}, a3+a8={answer}')
