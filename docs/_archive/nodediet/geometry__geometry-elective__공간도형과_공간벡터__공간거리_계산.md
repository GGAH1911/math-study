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

# 공간거리 계산

## 정확한 진술

공간의 두 점 $P(x_1, y_1, z_1)$과 $Q(x_2, y_2, z_2)$ 사이의 거리는 다음과 같이 정의됩니다.

$$\overline{PQ} = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$$

더 일반적으로, 공간에서 거리를 계산하는 경우는 다음을 포함합니다.
- **점과 평면 사이의 거리**: 평면 $ax+by+cz+d=0$ 위가 아닌 점 $P(x_0, y_0, z_0)$에서 평면까지의 거리는 $\frac{|ax_0+by_0+cz_0+d|}{\sqrt{a^2+b^2+c^2}}$
- **점과 직선 사이의 거리**: 직선 위의 한 점과 주어진 점을 이은 벡터가 직선의 방향벡터와 이루는 각을 이용

## 직관/기하적 의미

두 점 사이의 거리 공식은 **피타고라스 정리의 3차원 확장**입니다. 평면에서 직각삼각형을 이용해 $\sqrt{\Delta x^2 + \Delta y^2}$로 거리를 구했듯이, 공간에서는 한 축이 더 추가되어 $\sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2}$가 됩니다.

점과 평면 사이의 거리는 **평면에 수직인 방향으로만 측정**하므로, 법선벡터 방향의 정사영 길이를 이용합니다. 이는 최단거리를 나타냅니다.

## 한 줄 예

$P(1, 2, 3)$과 $Q(4, 6, 15)$ 사이의 거리는 $\sqrt{(4-1)^2+(6-2)^2+(15-3)^2} = \sqrt{9+16+144} = \sqrt{169} = 13$ (검증: `import sympy; sympy.sqrt(3**2 + 4**2 + 12**2)`)
