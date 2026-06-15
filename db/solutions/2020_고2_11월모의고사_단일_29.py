# f(x)=x²-2ax+a²-a+1, g: x+b (1<x<3), 7-b (x<=1 or x>=3). f·g 연속인 (a,b) 개수? a,b∈{1..5}
CANDIDATE = 7
count = 0
for a in range(1, 6):
    for b in range(1, 6):
        f1 = (a-1)*(a-2)            # f(1)
        f3 = (a-2)*(a-5)            # f(3)
        c1 = (f1 == 0) or (b == 3)  # x=1 연속: f(1)(7-b)=f(1)(1+b)
        c3 = (f3 == 0) or (b == 2)  # x=3 연속: f(3)(3+b)=f(3)(7-b)
        if c1 and c3:
            count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
