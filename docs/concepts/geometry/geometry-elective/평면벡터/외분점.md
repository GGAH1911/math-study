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

# 외분점

## 정확한 진술

두 점 $A$, $B$를 잇는 직선 위의 점 $P$가 $\overrightarrow{AP} : \overrightarrow{PB} = m : (-n)$ (단, $m > 0$, $n > 0$, $m \neq n$)을 만족할 때, 점 $P$를 선분 $AB$의 **외분점**이라 합니다. 이때 $m : n$을 **외분의 비**라 부릅니다. 

좌표로 나타내면, $A(x_1, y_1)$, $B(x_2, y_2)$일 때 외분점 $P$의 좌표는:
$$P = \left( \frac{mx_2 - nx_1}{m - n}, \frac{my_2 - ny_1}{m - n} \right)$$

## 직관과 기하적 의미

외분점은 두 점 $A$, $B$의 **바깥쪽**에 위치합니다. 내분점(두 점 사이)과 달리, 외분점은 연장선 상에서 한쪽 끝을 넘어섭니다. 

벡터로 이해하면, $\overrightarrow{AP}$와 $\overrightarrow{PB}$의 방향이 **반대**라는 뜻입니다. 따라서 위치벡터로는:
$$\vec{OP} = \frac{m\vec{OB} - n\vec{OA}}{m - n}$$

분모 $m - n$이 음수면 $P$는 $B$의 오른쪽에, 양수면 $A$의 왼쪽에 위치합니다.

## 한 줄 예와 검산

$A(1, 2)$, $B(5, 4)$를 $2 : 1$로 외분하는 점 $P$:
$$P = \left( \frac{2 \cdot 5 - 1 \cdot 1}{2 - 1}, \frac{2 \cdot 4 - 1 \cdot 2}{2 - 1} \right) = (9, 6)$$

검산: `from sympy import symbols, simplify; x1, y1, x2, y2, m, n = 1, 2, 5, 4, 2, 1; P = ((m*x2 - n*x1)/(m-n), (m*y2 - n*y1)/(m-n)); print(P)` 결과는 $(9, 6)$
