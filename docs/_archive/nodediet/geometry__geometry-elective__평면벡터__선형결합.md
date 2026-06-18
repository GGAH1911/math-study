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

# 선형결합

## 정확한 진술

두 개의 0이 아닌 벡터 $\vec{a}$, $\vec{b}$와 실수 $m$, $n$이 주어질 때, 다음과 같이 표현된 벡터를 $\vec{a}$와 $\vec{b}$의 **선형결합**이라 합니다:

$$\vec{c} = m\vec{a} + n\vec{b}$$

여기서 $m$, $n$을 **계수(coefficient)**라 부릅니다. 두 벡터가 일직선상에 있지 않으면(즉, 평면벡터가 선형독립이면), 평면 위의 모든 벡터는 이 두 벡터의 선형결합으로 유일하게 나타낼 수 있습니다.

## 직관과 기하적 의미

선형결합은 "주어진 두 방향을 각각 얼마나 가는가"를 조합하여 새로운 위치에 도달하는 개념입니다. 예를 들어 $\vec{a}$는 동쪽을 향한 변위, $\vec{b}$는 북쪽을 향한 변위라면, $2\vec{a} + 3\vec{b}$는 "동쪽으로 2배 이동한 후, 북쪽으로 3배 이동"한 최종 위치를 나타냅니다. 

기하학적으로, 계수 $m$, $n$을 변화시키면 선형결합 $m\vec{a} + n\vec{b}$는 전체 평면을 빠짐없이 채웁니다(단, $\vec{a}$와 $\vec{b}$가 선형독립일 때). 이는 좌표계의 근본 원리입니다.

## 한 줄 예

$\vec{a} = (1, 2)$, $\vec{b} = (2, -1)$일 때, $3\vec{a} + 2\vec{b} = 3(1, 2) + 2(2, -1) = (3, 6) + (4, -2) = (7, 4)$입니다.

**검산:** `sympy.Matrix([1, 2]) * 3 + sympy.Matrix([2, -1]) * 2` → $\begin{pmatrix} 7 \\ 4 \end{pmatrix}$
