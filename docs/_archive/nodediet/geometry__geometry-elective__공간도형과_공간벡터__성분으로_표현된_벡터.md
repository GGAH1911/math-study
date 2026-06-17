---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md]
enables: []
mastery: unknown
---

# 성분으로 표현된 벡터

좌표계의 기본단위벡터를 이용해 공간벡터를 좌표값들의 순서쌍으로 나타낸 표현입니다. 기하 공간벡터 단원의 표준 표기법입니다.

## 정의

공간 좌표계에서 표준기본단위벡터를 $\vec{i} = (1,0,0),\ \vec{j} = (0,1,0),\ \vec{k} = (0,0,1)$이라 할 때, 임의의 벡터 $\vec{u}$를 $\vec{u} = a\vec{i} + b\vec{j} + c\vec{k}$로 쓸 수 있으며 이를 **성분 표현**이라 합니다. 간단히 $\vec{u} = (a, b, c)$.

이때 벡터의 크기는
$$|\vec{u}| = \sqrt{a^2 + b^2 + c^2}.$$
두 벡터의 합, 스칼라배, 내적은 성분별로
- $(a_1, b_1, c_1) \pm (a_2, b_2, c_2) = (a_1 \pm a_2,\ b_1 \pm b_2,\ c_1 \pm c_2),$
- $k(a, b, c) = (ka, kb, kc),$
- $(a_1, b_1, c_1) \cdot (a_2, b_2, c_2) = a_1 a_2 + b_1 b_2 + c_1 c_2.$

## 예시

$\vec{u} = (2, -1, 2)$, $\vec{v} = (1, 0, -1)$에 대해 $|\vec{u}| = \sqrt{4+1+4} = 3$이고,
$$\vec{u} \cdot \vec{v} = 2 + 0 - 2 = 0$$
이므로 두 벡터는 서로 수직입니다.

## 관련 개념

- [공간각의 계산](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터/공간각의_계산.md)
- [공간도형과 공간벡터](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md)
