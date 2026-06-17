---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 수와식
grade: 중2
prerequisites: [docs/concepts/algebra/middle-2/식의_계산.md]
enables: []
mastery: unknown
---

# 복소수 상등성

두 복소수가 같다는 조건을 실수 부분과 허수 부분으로 분리하는 성질입니다. 미지수가 들어간 복소수 방정식 풀이의 기본 원리입니다.

## 정의

두 복소수 $a + bi$와 $c + di$ ($a, b, c, d$는 실수)에 대하여,
$$a + bi = c + di \iff a = c \text{ 그리고 } b = d.$$
특히 $a + bi = 0$이려면 $a = 0$이고 $b = 0$이어야 합니다.

## 예시

실수 $x, y$에 대하여 $(x + 2) + (y - 1)i = 5 + 3i$를 풀어 봅니다. 상등성에 의해 실수부와 허수부를 각각 같다고 놓으면 $x + 2 = 5$, $y - 1 = 3$이므로 $x = 3$, $y = 4$입니다.

또한 $(x + y) + (x - y)i = 4 + 2i$를 풀면 $x + y = 4$, $x - y = 2$에서 $x = 3$, $y = 1$입니다.

## 관련 개념

- [복소수 계산](docs/concepts/algebra/middle-2/식의_계산/복소수_기본.md)
- [복소수 켤레](docs/concepts/algebra/middle-2/식의_계산/복소수_기본.md)
- [식의 계산](docs/concepts/algebra/middle-2/식의_계산.md)
