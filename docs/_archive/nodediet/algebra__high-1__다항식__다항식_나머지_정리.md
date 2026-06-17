---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 수와식
grade: 고1
prerequisites: [docs/concepts/algebra/high-1/다항식.md]
enables: []
mastery: unknown
---

# 다항식 나머지 정리

다항식을 일차식 $x - \alpha$로 나누었을 때의 나머지를 직접 계산하지 않고 함숫값으로 얻는 정리입니다. 고1 다항식 단원의 핵심 정리이며 인수정리의 기초가 됩니다.

## 정의

다항식 $f(x)$를 일차식 $x - \alpha$로 나눈 나머지는 $f(\alpha)$입니다. 즉,
$$f(x) = (x - \alpha)\, Q(x) + R \implies R = f(\alpha).$$
일반적으로 $f(x)$를 $ax + b$ ($a \neq 0$)로 나눈 나머지는 $f\!\left(-\dfrac{b}{a}\right)$입니다.

## 예시

$f(x) = x^3 - 2x + 5$를 $x - 2$로 나눈 나머지를 구해 봅니다. 나머지 정리에 의해 나머지는 $f(2) = 8 - 4 + 5 = 9$입니다.

또한 $f(x) = 2x^2 - x + 3$을 $2x + 1$로 나눈 나머지는 $f\!\left(-\dfrac{1}{2}\right) = 2 \cdot \dfrac{1}{4} + \dfrac{1}{2} + 3 = 4$입니다.

## 관련 개념

- [다항식의 근](docs/concepts/algebra/high-1/다항식/다항식의_근.md)
- [나누어떨어짐](docs/concepts/algebra/high-1/다항식/나누어떨어짐.md)
- [다항식의 나눗셈](docs/concepts/algebra/high-1/다항식/나눗셈_정리.md)
