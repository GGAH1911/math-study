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

# 매개변수방정식

## 정확한 진술

매개변수방정식(parametric equation)은 곡선 위의 점을 하나의 독립변수 $t$의 함수로 나타낸 방정식입니다. 평면 위의 곡선이 다음 형태로 주어질 때:

$$x = f(t), \quad y = g(t) \quad (a \le t \le b)$$

여기서 $t$를 **매개변수(parameter)** 또는 **모수**라 부르고, $f(t)$와 $g(t)$는 연속함수입니다. 매개변수 $t$가 $a$에서 $b$로 변할 때, 점 $(x, y) = (f(t), g(t))$가 그리는 자취가 바로 이 곡선입니다.

## 직관적 의미

일반적으로 곡선을 $y = f(x)$ 형태로만 생각하면, 연직선(수직선)이 곡선과 두 점 이상에서 만나는 경우(예: 원, 타원)나 되돌아가는 궤적을 표현하기 어렵습니다. 매개변수방정식은 **시간 $t$에 따라 움직이는 점의 궤적**으로 곡선을 나타내므로, 이러한 제약을 극복할 수 있습니다. 

기하적으로는 매개변수 $t$를 시간이라 생각하면, 점이 곡선 위를 따라 움직이는 과정 자체를 모델링하는 것입니다. 이는 포물선 발사체, 행성의 공전 궤도, 곡선 운동 등 물리적 현상을 자연스럽게 표현합니다.

## 한 줄 예

원 $x^2 + y^2 = r^2$은 $x = r\cos t$, $y = r\sin t$ $(0 \le t \le 2\pi)$로 표현됩니다. `sympy로 검증: (r*cos(t))**2 + (r*sin(t))**2 = r**2`
