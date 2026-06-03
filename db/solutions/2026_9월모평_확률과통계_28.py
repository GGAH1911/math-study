def solve():
    count = 0
    for r in range(3):
        for b in range(3):
            for aY in range(4):
                for bY in range(4 - aY):
                    cY = 3 - aY - bY
                    for aP in range(4):
                        for bP in range(4 - aP):
                            cP = 3 - aP - bP
                            a_total = (1 if r==0 else 0)+(1 if b==0 else 0)+aY+aP
                            b_total = (1 if r==1 else 0)+(1 if b==1 else 0)+bY+bP
                            if a_total < 1 or b_total < 1:
                                continue
                            a_colors = (1 if r==0 else 0)+(1 if b==0 else 0)+(1 if aY>0 else 0)+(1 if aP>0 else 0)
                            if a_colors > 3:
                                continue
                            count += 1
    return count

res = solve()
print('VERIFY_PASS' if res == 746 else f'VERIFY_FAIL: got {res}')