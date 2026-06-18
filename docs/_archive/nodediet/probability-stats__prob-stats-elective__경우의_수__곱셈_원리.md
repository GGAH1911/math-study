---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 곱셈 원리

두 사건이 잇따라 일어나는 경우의 수가 각 단계의 경우의 수의 곱과 같다는 원리입니다. 확률과 통계 경우의 수 단원의 핵심 도구입니다.

## 정의

사건이 단계별로 일어나며 각 단계에서의 선택지가 서로 독립적으로 정해질 때, 단계 1에서 $a_1$가지, 단계 2에서 $a_2$가지, $\ldots$, 단계 $k$에서 $a_k$가지의 경우가 있다면 전체 경우의 수는
$$a_1 \times a_2 \times \cdots \times a_k.$$

이는 순열 계산과 직접 연결됩니다. 서로 다른 $n$개에서 $r$개를 택해 일렬로 배열하는 순열의 수는
$$_nP_r = n(n-1)(n-2)\cdots(n - r + 1) = \frac{n!}{(n - r)!}.$$

## 예시

서로 다른 셔츠 $3$벌, 바지 $4$벌, 신발 $2$켤레로 옷을 한 벌씩 골라 입는 방법의 수는 곱셈 원리로
$$3 \times 4 \times 2 = 24.$$

또한 서로 다른 $5$명 중 $2$명을 뽑아 일렬로 세우는 방법의 수는
$$_5P_2 = 5 \times 4 = 20.$$

## 관련 개념

- [경우의 수 기초](docs/concepts/probability-stats/prob-stats-elective/경우의_수/경우의_수_기초.md)
- [조합의 기본 계산](docs/concepts/probability-stats/high-1/경우의_수_고1/조합의_기본_계산.md)
- [경우의 수](docs/concepts/probability-stats/prob-stats-elective/경우의_수.md)
