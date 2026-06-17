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

# 속도와 거리의 관계

## 정확한 진술

물체가 시간 $t = a$부터 $t = b$까지 움직일 때, 속도 함수를 $v(t)$라 하면, 이 구간에서 이동한 거리(또는 변위)는

$$s = \int_a^b v(t) \, dt$$

입니다. 이는 **정적분이 넓이를 나타낸다**는 원리를 속도-시간 그래프에 적용한 것입니다.

## 직관과 기하적 의미

$t$축과 $v(t)$ 그래프 사이의 넓이가 바로 이동 거리입니다. 매우 작은 시간 간격 $\Delta t$ 동안 물체는 거의 일정한 속도 $v(t)$로 움직이므로, 이 짧은 순간의 거리는 $v(t) \cdot \Delta t$입니다. 이런 미소 거리들을 모두 더하면(적분) 전체 거리가 되는 것이죠.

**중요한 점:** 속도가 음수인 구간이 있으면 (즉, 물체가 반대 방향으로 움직이면), 정적분은 그 부분을 음수로 계산합니다. 따라서:
- **변위** = $\int_a^b v(t) \, dt$ (방향을 고려, 음수 가능)
- **이동 거리** = $\int_a^b |v(t)| \, dt$ (항상 양수)

## 한 줄 예

$v(t) = 3t$ m/s이고 $t = 0$부터 $t = 2$초까지 움직이면, 변위는 $\int_0^2 3t \, dt = \left[\frac{3t^2}{2}\right]_0^2 = 6$ m입니다. (`import sympy as sp; t = sp.Symbol('t'); sp.integrate(3*t, (t, 0, 2))`)
