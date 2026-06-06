from sympy import symbols, I, re, im, simplify

# 주어진 조건: 3z - 2*conjugate(z) = 5 + 10i
# z = a + bi로 놓고 풀어낸 결과: z = 5 + 2i
z = 5 + 2*I
z_conj = 5 - 2*I

# 원래 등식 검증
original_eq = 3*z - 2*z_conj
expected = 5 + 10*I

if simplify(original_eq - expected) == 0:
    # z*conjugate(z) 계산
    result = z * z_conj
    result_simplified = simplify(result)
    
    # 결과가 29인지 확인
    if result_simplified == 29:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')