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

# 분배

## 정확한 진술

분배란 구분되지 않는 여러 개의 동일한 대상을 구분되는 여러 개의 상자나 범주에 배치하는 것을 의미합니다. 가장 기본적인 형태는 **$n$개의 같은 공을 $r$개의 서로 다른 상자에 넣는 경우의 수**를 구하는 문제입니다. 이때 각 상자에는 0개 이상의 공을 넣을 수 있습니다. 이 경우의 수는 **중복조합** $H(n,r) = \binom{n+r-1}{r}$로 계산됩니다.

## 직관/기하적 의미

분배 문제의 핵심은 "무엇을 배치할 것인가"와 "어디에 배치할 것인가"를 구분하는 것입니다. 만약 배치할 대상들이 구분되지 않으면 (예: 동일한 사탕), 배치 방법의 수는 단순히 "각 상자에 몇 개씩 들어가는가"만 세면 됩니다. 이를 음이 아닌 정수해의 개수 문제로 변환할 수 있습니다. 

$x_1 + x_2 + \cdots + x_r = n$ (단, $x_i \geq 0$)

여기서 $x_i$는 $i$번째 상자에 들어가는 공의 개수입니다. 이 식의 음이 아닌 정수해의 개수가 바로 분배의 경우의 수입니다.

## 한 줄 예

같은 과자 5개를 A, B, C 세 친구에게 나누어 주는 경우의 수: $H(5,3) = \binom{5+3-1}{3} = \binom{7}{3} = 35$ (검증: `from sympy import binomial; binomial(7, 3)` → 35)
