---
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

# 두 평면이 이루는 각

## 정확한 진술

두 평면이 이루는 각은 두 평면의 법선벡터가 이루는 각의 크기(또는 그 여각)로 정의합니다. 두 평면의 법선벡터를 각각 $\vec{n}_1$, $\vec{n}_2$라 할 때, 두 평면이 이루는 각을 $\theta$라 하면:

$$\cos \theta = \frac{|\vec{n}_1 \cdot \vec{n}_2|}{|\vec{n}_1| \cdot |\vec{n}_2|}$$

여기서 $0 \leq \theta \leq \frac{\pi}{2}$ (또는 $0° \leq \theta \leq 90°$)입니다. 절댓값을 취하는 이유는 두 평면이 이루는 각을 항상 예각 또는 직각으로 정의하기 때문입니다.

## 직관과 기하적 의미

두 평면이 교선을 따라 만날 때, 그 사이의 "벌어진 정도"를 측정하는 것이 두 평면이 이루는 각입니다. 교선 위의 한 점에서 교선에 수직인 두 직선(각 평면 내에서)을 그으면, 이 두 직선이 이루는 각이 바로 두 평면이 이루는 각입니다. 

법선벡터를 사용하는 이유는 각 평면의 방향을 유일하게 결정하고, 복잡한 기하 작도 없이 벡터 연산만으로 각을 구할 수 있기 때문입니다. 절댓값을 사용하면 법선벡터의 방향 선택(위/아래)에 관계없이 같은 각을 얻습니다.

## 한 줄 예

평면 $\pi_1: 2x + y - z = 1$과 평면 $\pi_2: x - y + 2z = 3$이 이루는 각을 구하면, 법선벡터 $\vec{n}_1 = (2, 1, -1)$, $\vec{n}_2 = (1, -1, 2)$에 대해 $\cos \theta = \frac{|2 - 1 - 2|}{\sqrt{6} \cdot \sqrt{6}} = \frac{1}{6}$이므로 $\theta = \arccos(\frac{1}{6})$ 입니다.
```python
# sympy로 검증: cos_theta = 1/6 확인
import sympy as sp
n1 = sp.Matrix([2, 1, -1])
n2 = sp.Matrix([1, -1, 2])
cos_theta = abs(n1.dot(n2)) / (n1.norm() * n2.norm())
print(cos_theta)  # 1/6
```
