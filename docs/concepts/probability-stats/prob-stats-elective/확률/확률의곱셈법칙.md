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

# 확률의곱셈법칙

## 정확한 진술

두 사건 $A$, $B$에 대해 **확률의 곱셈법칙**은 다음과 같이 정의됩니다:

$$P(A \cap B) = P(A) \times P(B|A)$$

여기서 $P(B|A)$는 사건 $A$가 일어났을 때 사건 $B$가 일어날 **조건부확률**입니다. 만약 두 사건이 **독립**(서로 영향을 주지 않음)이면:

$$P(A \cap B) = P(A) \times P(B)$$

## 직관 및 의미

사건 $A$와 $B$가 **연쇄적으로** 일어난다고 생각해 봅시다. 먼저 $A$가 일어날 확률이 $P(A)$이고, $A$가 일어난 상황에서 $B$가 일어날 확률이 $P(B|A)$입니다. 전체 상황에서 둘 다 일어날 확률은 "먼저 $A$가 일어나고, 그 다음 $B$가 일어나야" 하므로, 두 확률을 곱하는 것이 자연스럽습니다.

**독립 사건의 경우**: $A$가 일어나든 안 일어나든 $B$의 확률이 변하지 않으므로 $P(B|A) = P(B)$가 되어 더 간단한 형태가 됩니다.

## 한 줄 예

검은 공 3개와 흰 공 2개가 들어있는 주머니에서 공을 하나씩 꺼낼 때, 처음엔 검은 공, 두 번째는 흰 공이 나올 확률은 $\frac{3}{5} \times \frac{2}{4} = \frac{3}{10}$입니다.

*(검증: 복원 없이 뽑을 때 $P(\text{검})=3/5$, $P(\text{흰}|\text{검})=2/4$)*
