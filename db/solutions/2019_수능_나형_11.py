from sympy import symbols, solve, S

x = symbols('x', real=True)

# ~p의 진리집합: 1 <= x <= 3
# q의 진리집합: x <= a
# 조건: ~P ⊆ Q, 즉 [1,3] ⊆ (-inf, a]
# a >= max(~P) = 3

# ~p 집합: [1, 3]
not_p_max = 3  # [1,3]의 최댓값

# a의 최솟값
a_min = not_p_max

# 검증: a=3 일 때 [1,3] ⊆ (-inf, 3] 인지 확인
a = a_min
not_p_set_max = 3
not_p_set_min = 1

if not_p_set_max <= a and not_p_set_min <= a:
    # a-1=2 일 때는 실패해야 함
    a_less = a - 1
    if not (not_p_set_max <= a_less):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
