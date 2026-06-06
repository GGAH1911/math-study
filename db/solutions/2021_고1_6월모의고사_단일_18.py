def verify():
    # 원래 문제 조건: (4x+2)^10 = x*Q(x) + R
    # x=0일 때: R = 2^10
    a = 2**10
    assert a == 1024, f'(가) = {a} should be 1024'
    
    # x=505일 때: 2022^10 = 505*Q(505) + 1024
    # 1024를 505로 나눈 몫과 나머지
    b = 1024 // 505  # 몫
    c = 1024 % 505   # 나머지
    
    assert b == 2, f'(나) = {b} should be 2'
    assert c == 14, f'(다) = {c} should be 14'
    
    # 검증: 1024 = 505 * b + c
    assert 505 * b + c == 1024, f'1024 != 505*{b} + {c}'
    
    # 최종 답
    result = a + b + c
    assert result == 1040, f'a+b+c = {result} should be 1040'
    
    print('VERIFY_PASS')

verify()