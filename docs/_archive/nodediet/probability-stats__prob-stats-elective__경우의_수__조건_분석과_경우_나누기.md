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

# 조건 분석과 경우 나누기

## 정확한 진술

조건 분석과 경우 나누기는 전체 경우들을 **특정 조건을 기준으로 상호배타적(겹치지 않는) 부분 경우들로 분류**한 후, 각 부분의 경우의 수를 따로 구해서 모두 더하는 방법입니다. 수식으로 쓰면, 전체 사건 $S$를 조건 $C_1, C_2, \ldots, C_n$에 따라 분할할 때:

$$n(S) = n(C_1) + n(C_2) + \cdots + n(C_n)$$

여기서 $C_i \cap C_j = \emptyset$ (조건들이 서로 겹치지 않음)이고 $C_1 \cup C_2 \cup \cdots \cup C_n = S$ (조건들의 합집합이 전체)입니다.

## 직관과 의미

복잡한 문제를 한 번에 세기는 어렵지만, **적절한 조건으로 나누면** 각 부분은 단순해집니다. 예를 들어 "주사위 두 개를 던져 합이 7 이상인 경우의 수"는 한 번에 세기 어렵지만, "첫 번째 주사위 눈깔(1, 2, 3, 4, 5, 6)"로 나누면 각 경우를 쉽게 셀 수 있습니다. 이것이 합의 법칙(덧셈 원리)의 핵심입니다.

## 한 줄 예

남자 5명, 여자 3명 중에서 1명을 선택하는 경우의 수는 "(남자 선택) 또는 (여자 선택)"으로 나누어 $5 + 3 = 8$가지입니다.
