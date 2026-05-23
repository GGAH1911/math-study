---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 확률통계
grade: 고1
prerequisites: [docs/concepts/probability-stats/high-1/경우의_수_고1.md]
enables: []
mastery: unknown
---

# 경우의 수 계산

어떤 사건이 일어나는 모든 경우의 수를 세는 절차로, 합의 법칙과 곱의 법칙을 기본 도구로 사용합니다. 고1 확률과 통계 단원의 출발점입니다.

## 정의

두 사건 $A, B$의 경우의 수에 대해
- **합의 법칙:** 두 사건이 동시에 일어나지 않으면(서로소), $A$ 또는 $B$가 일어나는 경우의 수는 $n(A) + n(B)$.
- **곱의 법칙:** 사건 $A$가 일어난 뒤 사건 $B$가 일어나는 경우의 수가 각각 $a, b$일 때, 두 사건이 연달아 일어나는 경우의 수는 $a \times b$.

복잡한 문제는 보통 단계별 분류(합의 법칙)와 순서대로의 선택(곱의 법칙)을 조합해 풉니다.

## 예시

서울에서 부산까지 가는 교통편이 기차 $2$가지, 버스 $3$가지, 비행기 $1$가지 있을 때 서울에서 부산까지 가는 경우의 수는 합의 법칙으로
$$2 + 3 + 1 = 6.$$

또한 동전 한 개와 주사위 한 개를 동시에 던질 때 나오는 경우의 수는 곱의 법칙으로 $2 \times 6 = 12$입니다.

## 관련 개념

- [경우의 수 기초](docs/concepts/probability-stats/prob-stats-elective/경우의_수/경우의_수_기초.md)
- [곱셈 원리](docs/concepts/probability-stats/prob-stats-elective/경우의_수/곱셈_원리.md)
- [경우의 수 (고1)](docs/concepts/probability-stats/high-1/경우의_수_고1.md)
