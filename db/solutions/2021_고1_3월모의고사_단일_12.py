pts=[(1,8),(1,6),(2,3),(3,7),(3,4),(3,3),(4,6),(5,8),(5,5),(5,4),(6,10),(6,5),(6,1),(7,9),(7,7),(7,6),(7,5),(8,2),(9,9),(9,5)]
a=sum(1 for x,y in pts if y>x)
b=sum(1 for x,y in pts if x>=5 and y>=5)
print('VERIFY_PASS' if len(pts)==20 and a==9 and b==10 and a+b==19 else 'VERIFY_FAIL')