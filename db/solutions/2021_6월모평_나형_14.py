from sympy import Rational

# memoized recursion using the original defining relations
memo = {1: Rational(1)}

def a(k):
    if k in memo:
        return memo[k]
    # determine which form k matches: 3n-1, 3n, 3n+1
    if (k + 1) % 3 == 0:        # k = 3n-1
        n = (k + 1) // 3
        val = 2 * a(n) + 1
    elif k % 3 == 0:            # k = 3n
        n = k // 3
        val = -a(n) + 2
    elif (k - 1) % 3 == 0:      # k = 3n+1
        n = (k - 1) // 3
        val = a(n) + 1
    else:
        raise ValueError('no form')
    memo[k] = val
    return val

result = a(11) + a(12) + a(13)
print('a11,a12,a13 =', a(11), a(12), a(13))
print('sum =', result)
print('VERIFY_PASS' if result == 8 else 'VERIFY_FAIL')
