vals=[]
for k in range(-20,30):
    cnt=0
    for x in range(-30,40):
        if abs(x-k)<=4 and x*x-11*x+18<0:
            cnt+=1
    if cnt==3:
        vals.append(k)
total=sum(vals)
print('VERIFY_PASS' if total==11 else 'VERIFY_FAIL')