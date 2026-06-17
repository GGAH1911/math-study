---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/이차곡선.md]
enables: []
mastery: unknown
---

# 점에서의 접선

## 정확한 진술

곡선 $C$ 위의 한 점 $P$에서의 **접선**(tangent line)은 점 $P$를 지나고, 곡선이 그 점에서 가지는 기울기와 같은 기울기를 가진 직선입니다. 이차곡선(포물선, 타원, 쌍곡선) 위의 점 $(x_0, y_0)$에서 접선의 방정식은, 곡선의 방정식을 $y$에 대해 미분한 도함수 $\frac{dy}{dx}$에 $x = x_0$을 대입하여 얻은 기울기 $m = \frac{dy}{dx}\bigg|_{x=x_0}$를 이용해 다음과 같이 나타냅니다:

$$y - y_0 = m(x - x_0)$$

예를 들어 포물선 $y = ax^2$에서 점 $(x_0, ax_0^2)$에서의 접선은 $\frac{dy}{dx} = 2ax$이므로 기울기가 $2ax_0$이 되어, 접선의 방정식은 $y - ax_0^2 = 2ax_0(x - x_0)$입니다.

## 직관/기하적 의미

곡선 위의 두 점 $P$와 $Q$를 잇는 **할선**(secant line)의 기울기는 $\frac{\Delta y}{\Delta x}$입니다. $Q$가 $P$에 가까워질수록 할선은 점 $P$에서 곡선이 가진 "순간 기울기"에 수렴하고, 이 극한값이 바로 미분계수입니다. 접선은 곡선이 한 점에서 "얼마나 빠르게 변하는가"를 나타내는 직선이며, 곡선과 그 점에서 **같은 방향**으로 진행합니다. 기하학적으로는 곡선과 그 점에서 한 번 만나고, 충분히 가까운 근처에서는 곡선과 겹치지 않는 직선입니다.

## 한 줄 예

포물선 $y = x^2$ 위의 점 $(2, 4)$에서의 접선: 기울기는 $\frac{dy}{dx}\big|_{x=2} = 2 \cdot 2 = 4$이므로 $y - 4 = 4(x - 2)$, 즉 $y = 4x - 4$입니다. (검증: `sympy.diff(x**2, x).subs(x, 2)` → 4)
