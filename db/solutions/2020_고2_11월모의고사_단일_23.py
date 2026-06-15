import sympy as sp
# y=log2(x+1)+2, 1<=x<=7 의 최댓값? (증가 → x=7)
CANDIDATE = 5
print('VERIFY_PASS' if sp.log(7+1, 2)+2 == CANDIDATE else 'VERIFY_FAIL')
