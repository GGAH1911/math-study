---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_미분.md]
enables: []
mastery: unknown
---

# 매개변수 함수의 미분

## 정확한 진술

매개변수 함수는 $x = f(t)$, $y = g(t)$ 형태로 주어진 곡선입니다. 여기서 $t$는 매개변수(parameter)이고, 점 $(x, y)$가 $t$에 따라 결정됩니다.

매개변수 함수에서 $\frac{dy}{dx}$를 구하려면 연쇄법칙을 사용합니다:

$$\frac{dy}{dx} = \frac{\frac{dy}{dt}}{\frac{dx}{dt}} = \frac{g'(t)}{f'(t)} \quad (f'(t) \neq 0)$$

## 직관과 기하적 의미

$t$를 시간으로 생각하면, 점 $(x, y)$는 시간에 따라 평면 위를 움직입니다. $\frac{dx}{dt}$는 수평 방향의 속도, $\frac{dy}{dt}$는 연직 방향의 속도입니다. 

두 속도의 비 $\frac{dy/dt}{dx/dt}$는 **궤적에 그은 접선의 기울기**가 됩니다. 즉, 매개변수 함수로 나타낸 곡선이 어느 점에서 얼마나 가파른지를 나타냅니다.

## 한 줄 예

$x = t^2$, $y = t^3$일 때, $\frac{dx}{dt} = 2t$, $\frac{dy}{dt} = 3t^2$이므로:

$$\frac{dy}{dx} = \frac{3t^2}{2t} = \frac{3t}{2} \quad (t \neq 0)$$

예를 들어 $t = 2$일 때 접선의 기울기는 $3$입니다. (`sympy.diff(t**3, t) / sympy.diff(t**2, t)` → $\frac{3t^2}{2t}$)
