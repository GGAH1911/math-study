---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 중3
prerequisites: [docs/concepts/functions/middle-3/이차함수.md]
enables: []
mastery: unknown
---

# 실근 존재 조건

이차방정식이 실수 해를 가지는지 여부를 판별식으로 결정하는 조건입니다. 중3 이차함수와 방정식 단원의 핵심 도구입니다.

## 정의

이차방정식 $ax^2 + bx + c = 0$ ($a \neq 0$)의 판별식 $D = b^2 - 4ac$에 대해
- $D > 0$: 서로 다른 두 실근.
- $D = 0$: 중근(서로 같은 두 실근).
- $D < 0$: 실근이 없음(서로 다른 두 허근).

따라서 "실근을 가질 조건"은 $D \ge 0$, "서로 다른 두 실근을 가질 조건"은 $D > 0$입니다.

## 예시

$x^2 - 4x + k = 0$이 서로 다른 두 실근을 갖도록 하는 $k$의 범위를 구해 봅니다. 판별식은
$$D = 16 - 4k.$$
$D > 0$이려면 $16 - 4k > 0$, 즉 $k < 4$입니다.

또한 $x^2 + 2x + k = 0$이 중근을 가지려면 $D = 4 - 4k = 0$, 즉 $k = 1$입니다.

## 관련 개념

- [이차함수의 판별식](docs/concepts/functions/middle-3/이차함수/이차함수의_판별식.md)
- [판별식과 중근](docs/concepts/functions/middle-3/이차함수/중근_조건.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
