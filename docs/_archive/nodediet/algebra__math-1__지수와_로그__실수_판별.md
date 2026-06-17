---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 수와식
grade: 수학1
prerequisites: [docs/concepts/algebra/math-1/지수와_로그.md]
enables: []
mastery: unknown
---

# 실수 판별

거듭제곱근이나 로그가 실수값으로 정의되는지 확인하는 절차입니다. 수학1 지수와 로그 단원에서 $n$제곱근의 정의 및 로그의 진수·밑 조건과 함께 다룹니다.

## 정의

- **거듭제곱근의 실수 조건:** 실수 $a$의 실수 $n$제곱근은, $n$이 홀수이면 항상 존재하고, $n$이 짝수이면 $a \ge 0$일 때에만 존재합니다.
- **로그의 실수 조건:** $\log_a b$가 실수로 정의되려면 밑 조건 $a > 0,\ a \neq 1$과 진수 조건 $b > 0$을 모두 만족해야 합니다.

## 예시

$\sqrt[4]{a-2}$가 실수가 되도록 하는 $a$의 범위를 구해 봅니다. $4$가 짝수이므로 피제곱수가 $0$ 이상이어야 합니다. 따라서 $a - 2 \ge 0$, 즉 $a \ge 2$입니다.

또한 $\log_{x-1}(5 - x)$가 정의되도록 하는 $x$의 범위는, 밑 조건 $x - 1 > 0$이고 $x - 1 \neq 1$, 진수 조건 $5 - x > 0$에서 $1 < x < 5$이고 $x \neq 2$입니다.

## 관련 개념

- [n제곱근의 정의](docs/concepts/algebra/math-1/지수와_로그/거듭제곱근.md)
- [지수와 로그](docs/concepts/algebra/math-1/지수와_로그.md)
