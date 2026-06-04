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

# 선분의 분할

## 정확한 진술

두 점 $A$, $B$가 주어졌을 때, 선분 $AB$ 위의 점 $P$가 $\overrightarrow{AP} : \overrightarrow{PB} = m : n$ (단, $m, n > 0$)을 만족하면, 점 $P$를 선분 $AB$를 $m : n$으로 **내분하는 점** 또는 **내분점**이라 합니다. 이때 점 $P$의 위치벡터는 다음과 같이 나타냅니다:

$$\overrightarrow{OP} = \frac{n \overrightarrow{OA} + m \overrightarrow{OB}}{m + n}$$

$m : n$의 순서를 반대로 하거나 음수를 허용하여, 선분을 연장한 직선 위의 점을 생각할 수 있습니다. 이를 **외분점**이라 하며, 선분 $AB$를 $m : n$ ($m > n > 0$)으로 외분하는 점 $Q$는:

$$\overrightarrow{OQ} = \frac{-n \overrightarrow{OA} + m \overrightarrow{OB}}{m - n}$$

## 직관과 기하적 의미

선분의 분할은 **가중평균(weighted average) 개념**입니다. 내분점은 두 위치벡터를 분할 비의 역비로 가중치를 두어 조합한 것입니다. 예를 들어 $m : n = 3 : 2$이면, 점 $P$는 $B$에 더 가깝고(가중치가 $3$), $A$에서의 거리는 상대적으로 더 깁니다(가중치가 $2$).

**직선 위의 점**이므로 $A$와 $B$ 사이를 오가며 움직이는 경우가 내분, 한쪽을 넘어서 연장되는 경우가 외분입니다. 이는 물리학의 무게중심 계산과 동일한 원리입니다.

## 한 줄 예

$\overrightarrow{OA} = (1, 2)$, $\overrightarrow{OB} = (4, 8)$일 때, 선분 $AB$를 $1 : 2$로 내분하는 점 $P$는 $\overrightarrow{OP} = \frac{2(1,2) + 1(4,8)}{1+2} = (2, 4)$입니다. (검산: `sympy.Matrix([2,4])`)
