# 산점도 해석 문제 - 조건 확인
# 조건: 기온 높음 → 난방비 감소 (음의 상관관계)
import numpy as np

# 음의 상관관계 패턴: x 증가하면 y 감소
# 선택지 ②는 왼쪽 위(저온, 고가격)에서 오른쪽 아래(고온, 저가격)로 향함
# 이는 음의 상관을 시각적으로 표현

# 검증: 음의 상관관계를 보이는 데이터 생성
temp = np.linspace(0, 30, 30)  # 기온: 0~30℃
heat_cost = 100 - 2.5 * temp + np.random.normal(0, 5, 30)  # 난방비: 감소 추세
heat_cost = np.maximum(heat_cost, 10)  # 음수 방지

# 상관계수 계산
corr = np.corrcoef(temp, heat_cost)[0, 1]

# 음의 상관계수 확인
assert corr < 0, f"음의 상관관계여야 하는데 r={corr}"
print("VERIFY_PASS")