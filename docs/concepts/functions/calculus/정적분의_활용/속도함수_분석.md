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

# 속도함수 분석

## 정의: 속도함수

시각 $t$에서의 물체의 속도를 나타내는 함수 $v(t)$를 **속도함수**라 한다. 물체의 위치를 나타내는 함수를 $s(t)$라 하면, 속도함수는 $v(t) = \frac{ds}{dt}$로 정의되며, 역으로 속도함수의 정적분으로부터 변위를 구할 수 있다:

$$s(b) - s(a) = \int_a^b v(t) \, dt$$

여기서 $[a, b]$는 시간 구간이고, $s(b) - s(a)$는 시각 $a$에서 $b$까지의 **변위**(방향을 포함한 위치 변화)이다. 속력 $|v(t)|$를 적분하면 **실제 이동 거리**를 얻는다:

$$\text{거리} = \int_a^b |v(t)| \, dt$$

## 직관 및 기하적 의미

$v(t)$의 그래프에서, 시간축 아래 넓이는 음수(음의 방향 이동)를 나타낸다. $\int_a^b v(t) \, dt$는 그래프가 시간축 위에 있는 부분의 넓이에서 아래에 있는 부분의 넓이를 뺀 값이므로, 이는 순변위(net displacement)를 의미한다. 

물리적으로, 속도함수는 시간에 따른 방향성 있는 움직임을 기술하며, 정적분은 이 움직임을 누적하여 최종 위치를 결정한다. 속력의 적분은 방향을 무시하고 실제로 움직인 총 거리를 나타낸다.

## 한 줄 예

$v(t) = 3t - 2$ (m/s)인 경우, $0$초부터 $3$초까지의 변위는:
$$\int_0^3 (3t-2) \, dt = \left[\frac{3t^2}{2} - 2t\right]_0^3 = \frac{27}{2} - 6 = \frac{15}{2} \text{ (m)}$$

(검산: `sympy.integrate(3*t - 2, (t, 0, 3))` → 7.5)
