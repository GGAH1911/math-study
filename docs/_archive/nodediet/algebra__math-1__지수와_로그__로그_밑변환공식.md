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

# 로그 밑변환공식

서로 다른 밑을 가진 로그를 같은 밑의 로그로 바꾸는 공식입니다. 수학1 지수와 로그 단원에서 로그값 계산과 식 변형의 핵심 도구입니다.

## 정의

$a > 0,\ a \neq 1,\ b > 0,\ c > 0,\ c \neq 1$일 때,
$$\log_a b = \frac{\log_c b}{\log_c a}.$$
특히 $c = b$로 두면 $\log_a b = \dfrac{1}{\log_b a}$를 얻습니다. 보통 상용로그($c = 10$)나 자연로그를 기준 밑으로 사용해 계산합니다.

## 예시

$\log_4 8$을 밑이 $2$인 로그로 바꾸어 계산해 봅니다.
$$\log_4 8 = \frac{\log_2 8}{\log_2 4} = \frac{3}{2}.$$

또한 $\log_2 5 \cdot \log_5 8$을 정리하면 밑변환공식과 $\log_5 8 = \dfrac{\log_2 8}{\log_2 5} = \dfrac{3}{\log_2 5}$에 의해
$$\log_2 5 \cdot \log_5 8 = \log_2 5 \cdot \frac{3}{\log_2 5} = 3.$$

## 관련 개념

- [로그값 계산](docs/concepts/algebra/math-1/지수와_로그/로그의_계산.md)
- [지수와 로그](docs/concepts/algebra/math-1/지수와_로그.md)
