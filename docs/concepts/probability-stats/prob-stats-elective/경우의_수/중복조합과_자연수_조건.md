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

# 중복조합과 자연수 조건

## 정확한 진술

$n$종류의 사물 중에서 중복을 허용하여 $r$개를 선택하는 조합의 개수를 **중복조합**이라 하고, $H(n, r)$ 또는 $\left(\!\left(\begin{array}{c} n \\ r \end{array}\right)\!\right)$로 나타낸다. 그 값은 다음 공식으로 주어진다.

$$H(n, r) = \binom{n+r-1}{r} = \binom{n+r-1}{n-1}$$

## 직관/기하적 의미

중복조합은 방정식 $x_1 + x_2 + \cdots + x_n = r$ (단, $x_i \geq 0$는 음이 아닌 정수)의 **정수해의 개수**와 정확히 일치한다. 이를 이해하는 가장 쉬운 방법은 "칸막이(stars and bars)" 논증이다. $r$개의 공을 $n$개의 상자에 넣는 상황을 생각하면, $n-1$개의 칸막이로 구분하면 된다. 따라서 총 $r + (n-1)$개 위치 중 칸막이 $n-1$개를 배치하는 경우의 수이므로 $\binom{r+n-1}{n-1}$이 된다.

예를 들어, 같은 종류의 사탕 6개를 3명에게 나누어 주는 방법의 수는 $x_1 + x_2 + x_3 = 6$ (단, $x_i \geq 0$)의 음이 아닌 정수해 개수이고, 이는 $H(3, 6) = \binom{8}{2} = 28$이다.

## 한 줄 예

방정식 $x + y + z = 5$의 음이 아닌 정수해 개수는 $H(3, 5) = \binom{7}{2} = 21$이다. (`sympy.binomial(7, 2)`)
