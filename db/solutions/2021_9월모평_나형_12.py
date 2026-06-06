from fractions import Fraction
se=Fraction(5,6)
m=Fraction(3925,100)
z=(Fraction(38)-m)/se
# z should be -1.5, giving P=0.5+0.4332=0.9332
if z==Fraction(-3,2):
    prob=0.5+0.4332
    print('VERIFY_PASS' if abs(prob-0.9332)<1e-9 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')