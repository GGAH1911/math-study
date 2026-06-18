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

# 경우의 수 기초

어떤 사건이 일어나는 모든 경우의 가짓수를 세는 가장 기본적인 두 법칙입니다. 확률과 통계 경우의 수 단원의 출발점입니다.

## 정의

- **합의 법칙(또는 가짓수의 덧셈):** 두 사건 $A, B$가 동시에 일어나지 않을 때(서로소), "$A$ 또는 $B$"가 일어나는 경우의 수는
$$n(A \cup B) = n(A) + n(B).$$
- **곱의 법칙(또는 가짓수의 곱):** 사건 $A$가 일어나는 경우의 수가 $a$, $A$가 일어난 후 사건 $B$가 일어나는 경우의 수가 $b$로 일정할 때, 두 사건이 연달아 일어나는 경우의 수는 $a \times b$.

문제에 따라 단계로 분리(곱의 법칙)할지, 경우로 분리(합의 법칙)할지를 명확히 구분해 적용하는 것이 핵심입니다.

## 예시

서울에서 대구로 가는 방법이 기차 $3$가지, 버스 $2$가지일 때 서울에서 대구로 가는 경우의 수는 합의 법칙으로 $3 + 2 = 5$입니다.

또한 서울→대구로 가는 방법 $5$가지, 대구→부산으로 가는 방법 $4$가지일 때 서울→대구→부산의 경로의 수는 곱의 법칙으로 $5 \times 4 = 20$입니다.

## 관련 개념

- [곱셈 원리](docs/concepts/probability-stats/prob-stats-elective/경우의_수/곱의_법칙과_합의_법칙.md)
- [경로의 수](docs/concepts/probability-stats/prob-stats-elective/경우의_수.md)
- [경우의 수](docs/concepts/probability-stats/prob-stats-elective/경우의_수.md)
