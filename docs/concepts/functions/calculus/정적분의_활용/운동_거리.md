---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 운동 거리

## 정확한 진술

시각 $t$에서의 속도를 $v(t)$라고 할 때, 시각 $a$부터 $b$까지 운동한 거리 $s$는 다음과 같이 정의됩니다:

$$s = \int_a^b |v(t)| \, dt$$

여기서 절댓값 기호가 중요합니다. 거리는 항상 양수이기 때문에, 속도가 음수인 구간(역방향 이동)에서도 이동한 경로의 길이를 더해야 합니다.

## 직관 및 기하적 의미

속도-시간 그래프에서 $|v(t)|$의 그래프 아래 넓이가 바로 운동한 거리입니다. 

만약 절댓값을 무시하고 $\int_a^b v(t) \, dt$로만 계산하면 **변위(displacement)**를 구하게 되는데, 이는 시작점에서 끝점까지의 직선거리입니다. 예를 들어 앞으로 10m 갔다가 뒤로 10m 돌아오면 변위는 0이지만, 운동한 거리는 20m입니다.

따라서:
- 속도의 부호가 바뀌지 않으면: $s = \left| \int_a^b v(t) \, dt \right| = \int_a^b |v(t)| \, dt$
- 속도의 부호가 바뀌면: 절댓값이 필수적으로 필요함

## 한 줄 예

$v(t) = 3t - 6$ (단위: m/s)이고, $t=0$부터 $t=4$초까지 움직일 때, 운동한 거리는 $\int_0^2 |3t-6| \, dt + \int_2^4 |3t-6| \, dt = \int_0^2 (6-3t) \, dt + \int_2^4 (3t-6) \, dt = 6 + 6 = 12$ m입니다.

(검증: `sympy.integrate(abs(3*t - 6), (t, 0, 4))` = 12)
