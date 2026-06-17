---
unit: 평면벡터
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md]
enables: []
mastery: unknown
---

# 벡터의 각도

## 정확한 진술

두 벡터 $\vec{a}$, $\vec{b}$가 주어질 때, 두 벡터가 이루는 각을 $\theta$라 하자 ($0 \le \theta \le \pi$). 두 벡터의 내적과 크기로부터, 두 벡터 사이의 각은 다음과 같이 정의된다:

$$\cos\theta = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}||\vec{b}|}$$

(단, $|\vec{a}| \neq 0$, $|\vec{b}| \neq 0$)

여기서 $\vec{a} \cdot \vec{b}$는 두 벡터의 내적이고, 이는 $\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$의 변형이다.

## 직관과 기하적 의미

이 정의는 두 화살표가 같은 시작점에서 출발할 때 벌어진 정도를 수치화한다. 코사인 함수의 성질에 의해:

- $\theta = 0$일 때: $\cos\theta = 1$ → 두 벡터가 같은 방향
- $0 < \theta < \frac{\pi}{2}$일 때: $\cos\theta > 0$ → 둔각보다 예각, 내적이 양수
- $\theta = \frac{\pi}{2}$일 때: $\cos\theta = 0$ → 두 벡터가 수직(직교)
- $\frac{\pi}{2} < \theta \le \pi$일 때: $\cos\theta < 0$ → 둔각, 내적이 음수
- $\theta = \pi$일 때: $\cos\theta = -1$ → 두 벡터가 반대 방향

내적 공식은 벡터의 기하학적 성질(방향, 크기)과 좌표를 이용한 대수적 계산을 연결하는 다리 역할을 한다.

## 계산 예

$\vec{a} = (1, 2)$, $\vec{b} = (3, 1)$일 때, $\vec{a} \cdot \vec{b} = 1 \cdot 3 + 2 \cdot 1 = 5$이고, $|\vec{a}| = \sqrt{1^2 + 2^2} = \sqrt{5}$, $|\vec{b}| = \sqrt{3^2 + 1^2} = \sqrt{10}$이다. 따라서:

$$\cos\theta = \frac{5}{\sqrt{5} \cdot \sqrt{10}} = \frac{5}{\sqrt{50}} = \frac{\sqrt{2}}{2}$$

이므로 $\theta = \frac{\pi}{4}$ (45°).

```python
# 검산 (sympy)
from sympy import *
a = Matrix([1, 2])
b = Matrix([3, 1])
cos_theta = a.dot(b) / (a.norm() * b.norm())
theta = acos(cos_theta)  # π/4
```
