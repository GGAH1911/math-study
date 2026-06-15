# 2020 9월모평 나형 02 (객관식): A={2,3,4}, B={1,a}, n(A∩B)=1. 모든 a의 합? (보기 ⑤=9)
CANDIDATE = 9                      # 정답 보기 ⑤ 의 값 (2+3+4)
A = {2, 3, 4}
valid = [a for a in range(1, 100) if len(A & {1, a}) == 1]   # a 자연수
print('VERIFY_PASS' if sum(valid) == CANDIDATE else 'VERIFY_FAIL')
