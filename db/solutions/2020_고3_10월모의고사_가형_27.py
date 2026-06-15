# f(0)=0,f(2)=1, A=B → ∫₀²f=0. ∫₀²(2x+3)f'(x)dx (부분적분)?
CANDIDATE = 7
f0, f2, If = 0, 1, 0            # ∫₀² f = 0
val = (2*2+3)*f2 - (2*0+3)*f0 - 2*If   # [(2x+3)f]₀² - ∫2f
print('VERIFY_PASS' if val == CANDIDATE else 'VERIFY_FAIL')
