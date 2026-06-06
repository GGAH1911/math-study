from fractions import Fraction

CANDIDATE = 80

# 문제 조건 인코딩
# A: 카드 1, 8 (각 1/2 확률)
# B: 카드 2, 3, 4, 5, 6, 7 (각 1/6 확률)

# 내려놓을 조건:
# - A는 8을 뽑을 때만 내려놓음: P(A 내려놓음) = 1/2
# - B는 n 이하 카드를 뽑을 때만 내려놓음: P(B 내려놓음) = (n-1)/6

# 점수 판정:
# - A만 내려놓음 → A 점수
# - B만 내려놓음 → B 점수
# - 둘 다 내려놓음 → A=8, B≤7이므로 B가 점수
# - 아무도 내려놓지 않음 → 점수 없음

def solve():
    # p = P(A가 점수 받음) = P(A 내려놓음 & B 내려놓지 않음)
    # q = P(B가 점수 받음) = P(B만 내려놓음) + P(둘 다 내려놓음)
    #                      = P(A 내려놓지 않음 & B 내려놓음) + P(A 내려놓음 & B 내려놓음)
    
    # p = q 조건에서 n 찾기
    for n in range(1, 8):
        p_a_puts = Fraction(1, 2)  # A가 카드 8을 뽑을 확률
        p_b_puts = Fraction(n - 1, 6)  # B가 n 이하 카드를 뽑을 확률
        p_b_not_puts = Fraction(7 - n, 6)  # B가 n보다 큰 카드를 뽑을 확률
        
        p = p_a_puts * p_b_not_puts  # A만 내려놓을 확률
        q = Fraction(1, 2) * p_b_puts + p_a_puts * p_b_puts  # B가 점수 받을 확률
        
        # p = q 확인
        if p == q:
            # 검증: 이 n에 대해 24(n+p) 계산
            value = 24 * (n + p)
            return value
    
    return None

result = solve()

# 엄격한 검증: 원래 식으로부터 유도한 값이 CANDIDATE와 일치하는지 확인
if result is not None and result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")