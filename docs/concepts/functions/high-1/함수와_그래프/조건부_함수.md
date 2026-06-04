---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 고1
prerequisites: [docs/concepts/functions/high-1/함수와_그래프.md]
enables: []
mastery: unknown
---

# 조건부 함수

## 정확한 진술

조건부 함수는 정의역을 여러 부분으로 나누어, 각 부분에서 서로 다른 식으로 정의되는 함수입니다. 일반적으로 다음과 같이 표현합니다.

$$f(x) = \begin{cases} f_1(x) & \text{if } x \in D_1 \\ f_2(x) & \text{if } x \in D_2 \\ \vdots & \vdots \\ f_n(x) & \text{if } x \in D_n \end{cases}$$

여기서 $D_1, D_2, \ldots, D_n$은 서로 겹치지 않는 구간들이고, $D_1 \cup D_2 \cup \cdots \cup D_n$이 정의역을 이룹니다. 각 $f_i$는 해당 구간에서 정의된 함수이며, 입력값 $x$가 어느 구간에 속하는지에 따라 적용할 식을 결정합니다.

## 직관과 기하적 의미

실생활에서는 상황이 바뀌면 규칙도 바뀝니다. 예를 들어 택시 요금은 거리 5km까지는 기본요금이 일정하고, 5km를 넘으면 거리에 따라 추가 요금을 계산합니다. 조건부 함수는 이런 **상황에 따른 규칙의 변화**를 수학으로 나타냅니다.

그래프로 보면 여러 조각이 합쳐진 모양입니다. 각 구간마다 다른 곡선(직선, 포물선 등)을 그리고, 경계점에서 연결되거나 끊어질 수 있습니다. 특히 경계점에서 **연속인지 불연속인지** 확인하는 것이 중요합니다.

## 한 줄 예

$f(x) = \begin{cases} x^2 & \text{if } x < 0 \\ 2x & \text{if } 0 \le x \le 3 \\ 9 & \text{if } x > 3 \end{cases}$는 조건부 함수로, $x$의 값에 따라 완전히 다른 규칙으로 함숫값을 계산합니다. 예를 들어 $f(-1) = 1$, $f(2) = 4$, $f(5) = 9$입니다. (sympy로 확인: `f = lambda x: x**2 if x < 0 else (2*x if x <= 3 else 9); [f(-1), f(2), f(5)]` → `[1, 4, 9]`)
