---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/평면벡터.md]
enables: []
mastery: unknown
---

# 벡터 성분

## 정확한 진술

평면의 벡터 $\vec{a}$를 정하는 가장 기본적인 방법은 좌표계를 이용하여 두 개의 수로 나타내는 것입니다. 원점을 시작점으로 하는 벡터 $\vec{a}$의 끝점이 $(a_1, a_2)$일 때, $a_1$을 **x-성분**, $a_2$를 **y-성분**이라 하며, 벡터를 다음과 같이 나타냅니다:

$$\vec{a} = \begin{pmatrix} a_1 \\ a_2 \end{pmatrix} \text{ 또는 } \vec{a} = (a_1, a_2)$$

더 일반적으로, 시작점 $P(x_1, y_1)$에서 끝점 $Q(x_2, y_2)$로 향하는 벡터 $\overrightarrow{PQ}$의 성분은:

$$\overrightarrow{PQ} = \begin{pmatrix} x_2 - x_1 \\ y_2 - y_1 \end{pmatrix}$$

## 직관과 기하적 의미

벡터의 성분은 벡터를 **x축과 y축 방향으로 얼마나 이동하는가**를 나타냅니다. 예를 들어, 성분이 $(3, 2)$인 벡터는 오른쪽으로 3칸, 위쪽으로 2칸 이동함을 의미합니다. 

이렇게 성분으로 표현하면, 벡터 간의 합, 차, 스칼라배를 계산하기가 매우 편리합니다. 또한 벡터의 크기(길이)도 성분으로부터 바로 구할 수 있습니다. 벡터 $\vec{a} = (a_1, a_2)$의 크기는:

$$|\vec{a}| = \sqrt{a_1^2 + a_2^2}$$

## 한 줄 예

시작점 $A(1, 2)$에서 끝점 $B(4, 5)$로 향하는 벡터 $\overrightarrow{AB}$의 성분은 $(4-1, 5-2) = (3, 3)$이고, 크기는 $\sqrt{3^2 + 3^2} = 3\sqrt{2}$입니다.

```python
# 검산: sympy.sqrt(3**2 + 3**2)
```
