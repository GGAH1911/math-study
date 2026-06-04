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

# 속도와 위치의 관계

## 정확한 진술

시간 $t$에서 위치를 나타내는 함수를 $s(t)$, 속도를 나타내는 함수를 $v(t)$라 할 때, 속도는 위치의 도함수입니다.

$$v(t) = \frac{ds}{dt}$$

역으로, $t_1$에서 $t_2$까지의 위치 변화(변위)는 속도를 시간에 대해 정적분한 값입니다.

$$s(t_2) - s(t_1) = \int_{t_1}^{t_2} v(t) \, dt$$

초기 위치 $s(t_0) = s_0$가 주어지면, 임의의 시각 $t$에서 위치는 다음과 같이 복원됩니다.

$$s(t) = s_0 + \int_{t_0}^{t} v(\tau) \, d\tau$$

## 직관과 기하적 의미

속도는 위치가 시간에 따라 얼마나 빨리 변하는지를 나타냅니다. 따라서 속도 함수를 시간에 대해 적분하면, 그 기간 동안 물체가 얼마나 이동했는지(변위)를 알 수 있습니다.

속도-시간 그래프에서, $t_1$부터 $t_2$까지의 곡선 아래 넓이가 바로 그 구간에서의 변위입니다. 이는 미적분의 기본 정리(fundamental theorem of calculus)의 실제 응용으로, 순간 변화율(속도)을 누적하면 전체 변화(위치 변화)가 된다는 의미입니다.

## 한 줄 예

어떤 물체의 속도가 $v(t) = 3t^2$ (단위: m/s)이고 초기 위치가 $s(0) = 5$ m일 때, $t = 2$초에서의 위치는 $s(2) = 5 + \int_0^2 3t^2 \, dt = 5 + 8 = 13$ m입니다. (`sympy.integrate(3*t**2, (t, 0, 2))` → 8)
