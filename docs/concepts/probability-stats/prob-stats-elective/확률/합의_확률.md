---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/확률.md]
enables: []
mastery: unknown
---

# 합의 확률

## 정확한 진술

두 사건 $A$와 $B$에 대해, **"$A$가 일어나거나 $B$가 일어나거나 둘 다 일어날 확률"**을 **합의 확률** 또는 **합사건의 확률**이라 부르며, 다음 공식으로 정의합니다:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

여기서 $P(A \cup B)$는 합의 확률, $P(A \cap B)$는 두 사건이 **동시에** 일어날 확률입니다.

**배타적 사건의 경우**: 두 사건이 동시에 일어날 수 없다면($A \cap B = \emptyset$) $P(A \cap B) = 0$이므로:
$$P(A \cup B) = P(A) + P(B)$$

## 직관과 기하적 의미

$P(A)$와 $P(B)$를 단순히 더하면, 두 사건이 동시에 일어나는 영역(교집합)이 **두 번 세어집니다**. 따라서 중복된 부분을 한 번 빼야만 정확한 합의 확률을 얻습니다. 벤다이어그램으로 생각하면, 두 원판의 합집합 넓이는 각각의 넓이를 더한 후 겹치는 부분을 한 번 뺀 것과 같은 원리입니다.

## 한 줄 예

주사위 한 개를 던질 때, $A$ = "3 이상의 수가 나옴", $B$ = "짝수가 나옴"이라 하면:
- $P(A) = \frac{4}{6}$ (3, 4, 5, 6)
- $P(B) = \frac{3}{6}$ (2, 4, 6)  
- $P(A \cap B) = \frac{2}{6}$ (4, 6)

따라서 $P(A \cup B) = \frac{4}{6} + \frac{3}{6} - \frac{2}{6} = \frac{5}{6}$

검증: 3 이상 또는 짝수 = {2, 3, 4, 5, 6} → $\frac{5}{6}$ ✓  
(`sympy.Rational(4,6) + sympy.Rational(3,6) - sympy.Rational(2,6)`)
