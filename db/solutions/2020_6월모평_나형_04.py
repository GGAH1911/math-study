# 2020 6월모평 나형 4번
# 그림: 함수 f: X -> X (X = {1,2,3,4}) 의 화살표 대응
#   왼쪽 1 -> 오른쪽 2   (f(1) = 2)
#   왼쪽 2 -> 오른쪽 3   (f(2) = 3)
#   왼쪽 3 -> 오른쪽 1   (f(3) = 1)
#   왼쪽 4 -> 오른쪽 4   (f(4) = 4)
# 묻는 값: f(1) + f^{-1}(3)
# 보기: (1) 3  (2) 4  (3) 5  (4) 6  (5) 7  -> 정답 (2) 4
CANDIDATE = 4  # option (2)

# --- 문제 조건을 코드로 인코딩 (그림의 대응) ---
X = [1, 2, 3, 4]
f = {1: 2, 2: 3, 3: 1, 4: 4}  # 화살표 대응 그대로

# f 는 X -> X 인 함수여야 한다 (정의역/치역 점검)
assert set(f.keys()) == set(X), "정의역이 X 가 아님"
assert all(v in X for v in f.values()), "치역이 X 를 벗어남"

# 역함수가 존재하려면 (역함수값을 읽으려면) f 는 일대일대응이어야 한다
assert len(set(f.values())) == len(X), "f 가 일대일대응이 아님 -> 역함수 정의 불가"

# 역함수: f(a) = b 인 a 를 b 에 대응
f_inv = {v: k for k, v in f.items()}

# 문제에서 묻는 식: f(1) + f^{-1}(3)
value = f[1] + f_inv[3]

print("VERIFY_PASS" if value == CANDIDATE else "VERIFY_FAIL")
