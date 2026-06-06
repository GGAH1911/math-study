# 수열 계산
a = {1: 1}

def compute_term(n):
    if n in a:
        return a[n]
    # n = 3m-1 형태인지 확인
    if (n + 1) % 3 == 0:
        m = (n + 1) // 3
        a[n] = 2 * compute_term(m) + 1
    # n = 3m 형태인지 확인
    elif n % 3 == 0:
        m = n // 3
        a[n] = -compute_term(m) + 2
    # n = 3m+1 형태인지 확인
    else:  # n % 3 == 1
        m = (n - 1) // 3
        a[n] = compute_term(m) + 1
    return a[n]

# a_11, a_12, a_13 계산
a11 = compute_term(11)
a12 = compute_term(12)
a13 = compute_term(13)

result = a11 + a12 + a13
print(f'a_11 = {a11}, a_12 = {a12}, a_13 = {a13}')
print(f'a_11 + a_12 + a_13 = {result}')

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')