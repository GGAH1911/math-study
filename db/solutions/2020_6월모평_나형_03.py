# 2020 6월모평 나형 03 (객관식): A={2,a}, B={1,2,3,5,7}, A∪B={1,2,3,5,7,9}. a? (보기 ⑤=9)
CANDIDATE = 9                      # 정답 보기 ⑤ 의 값
B = {1, 2, 3, 5, 7}
target = {1, 2, 3, 5, 7, 9}
A = {2, CANDIDATE}
print('VERIFY_PASS' if A | B == target else 'VERIFY_FAIL')
