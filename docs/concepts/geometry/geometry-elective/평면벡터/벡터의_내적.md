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

# 벡터의 내적

## 정확한 진술

두 벡터 $\vec{a} = (a_1, a_2)$, $\vec{b} = (b_1, b_2)$의 **내적**(또는 스칼라곱)은 다음과 같이 정의합니다:

$$\vec{a} \cdot \vec{b} = a_1 b_1 + a_2 b_2$$

또는 두 벡터의 크기와 사이각으로도 표현합니다:

$$\vec{a} \cdot \vec{b} = |\vec{a}| \cdot |\vec{b}| \cdot \cos \theta$$

여기서 $\theta$는 두 벡터 사이의 각입니다.

## 직관/기하적 의미

벡터의 내적은 **한 벡터가 다른 벡터 방향으로 얼마나 강하게 작용하는지**를 나타냅니다. 

물리학에서는 일(work)을 계산할 때 사용합니다. 예를 들어, 힘 벡터 $\vec{F}$가 물체를 변위 벡터 $\vec{s}$ 방향으로 움직일 때, 실제로 한 일은 $\vec{F} \cdot \vec{s}$입니다. 두 벡터가 같은 방향일수록 내적이 크고, 수직일 때는 0, 반대 방향일 때는 음수입니다.

기하학적으로는, $\vec{a} \cdot \vec{b} = |\vec{a}| \cdot (\vec{b}$의 $\vec{a}$ 방향 성분)으로 해석할 수 있습니다.

## 한 줄 예

$\vec{a} = (2, 3)$, $\vec{b} = (1, -1)$일 때, $\vec{a} \cdot \vec{b} = 2 \times 1 + 3 \times (-1) = -1$입니다. (검증: `sympy.Matrix([2, 3]).dot(sympy.Matrix([1, -1]))`)

두 벡터가 수직인지 판정할 때도 유용합니다. $\vec{a} \cdot \vec{b} = 0$이면 두 벡터는 수직입니다.
