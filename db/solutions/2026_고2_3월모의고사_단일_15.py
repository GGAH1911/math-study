def count_solutions(a):
    # integers x with x^2-2x-3 >= 0 AND (x+a)(x-a+2) < 0
    cnt = 0
    # range bounded by inequality
    lo = min(-a, a-2)
    hi = max(-a, a-2)
    for x in range(lo-1, hi+2):
        if x*x - 2*x - 3 >= 0 and (x+a)*(x-a+2) < 0:
            cnt += 1
    return cnt

good = [a for a in range(-50, 51) if count_solutions(a) == 6]
print('good a:', good)
print('sum:', sum(good))
print('VERIFY_PASS' if sum(good) == 2 else 'VERIFY_FAIL')
