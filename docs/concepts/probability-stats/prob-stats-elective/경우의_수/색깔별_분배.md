---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 색깔별 분배

## 정확한 진술

n개의 서로 다른 객체를 k가지 색깔로 칠하거나 k개의 구별되는 그룹으로 분배할 때, 각 객체가 독립적으로 k가지 색(또는 그룹) 중 하나를 선택할 수 있는 경우의 수는 $k^n$입니다.

더 일반적으로, n개의 서로 다른 객체를 k가지 색깔로 분류하되 각 색깔별로 정확히 $n_1, n_2, \ldots, n_k$개씩 분배하는 경우의 수는 **다항계수**(multinomial coefficient)로 표현됩니다:
$$\binom{n}{n_1, n_2, \ldots, n_k} = \frac{n!}{n_1! n_2! \cdots n_k!}$$
여기서 $n_1 + n_2 + \cdots + n_k = n$입니다.

## 직관·기하적 의미

색깔별 분배는 본질적으로 객체들을 여러 범주(색깔, 그룹, 상자)로 **분류하는 과정**입니다. 제약 조건이 없으면 각 객체는 독립적으로 선택하므로 곱의 법칙에 의해 $k^n$가지입니다. 하지만 각 색깔별 개수가 정해지면, 어떤 객체를 어느 색으로 할지 **순서대로 결정**하는 과정이 되고, 이때 같은 색의 객체들은 구별되지 않으므로 다항계수로 나눕니다.

## 한 줄 예

6개의 서로 다른 공을 빨강, 파랑, 노랑 3가지 색으로 자유롭게 칠하면 $3^6 = 729$가지이지만, 빨강 2개, 파랑 2개, 노랑 2개로 정확히 칠해야 한다면 $\frac{6!}{2! \cdot 2! \cdot 2!} = 90$가지입니다. (검산: `sympy.factorial(6) // (sympy.factorial(2) * sympy.factorial(2) * sympy.factorial(2))` = 90)
