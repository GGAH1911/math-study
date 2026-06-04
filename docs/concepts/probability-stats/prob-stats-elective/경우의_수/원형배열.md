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

# 원형배열

## 정확한 진술

원형배열(circular permutation)이란 n개의 서로 다른 원소를 원형으로 배열하되, 회전하여 같아지는 배열들을 하나로 보는 배열 방법입니다. n개의 서로 다른 원소의 원형배열의 가짓수는:

$$\text{원형배열의 수} = (n-1)!$$

## 직관/기하적 의미

먼저 n개의 원소를 일렬로 배열하면 n!가지입니다. 그런데 원형 배열은 시작점이라는 개념이 없습니다. 원탁에 앉은 네 사람 A, B, C, D를 생각해봅시다. 시계 방향으로 (A-B-C-D), (B-C-D-A), (C-D-A-B), (D-A-B-C)로 앉은 것은 모두 같은 배열입니다. 원탁에는 "맨 앞"이 없기 때문입니다.

한 배열은 n번 회전시킬 수 있으므로, n!개의 일렬 배열이 각각 n번씩 중복으로 세어집니다. 따라서 원형배열의 수는:

$$\frac{n!}{n} = (n-1)!$$

이 원리는 원탁 회의, 목걸이 디자인, 원형 시뮤레이션 등 일상의 많은 상황에 적용됩니다.

## 한 줄 예

4명이 원탁에 앉는 경우의 수는 $(4-1)! = 3! = 6$가지입니다.

검증: `sympy.factorial(3)` = 6
