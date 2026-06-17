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

# 나누어떨어짐

다항식의 나눗셈에서 나머지가 $0$이 되는 경우를 가리키는 개념입니다. 인수정리와 직접 연결되며, 다항식의 인수분해와 근 판별에 활용됩니다.

## 정의

두 다항식 $f(x), g(x)$ ($g(x) \neq 0$)에 대하여 $f(x) = g(x) \cdot Q(x)$를 만족시키는 다항식 $Q(x)$가 존재할 때, $f(x)$는 $g(x)$로 **나누어떨어진다**고 합니다. 이는 $f(x)$를 $g(x)$로 나누었을 때의 나머지가 $0$인 것과 동치입니다.

특히 인수정리에 의해 $f(x)$가 $(x - \alpha)$로 나누어떨어지는 것은 $f(\alpha) = 0$과 동치입니다.

## 예시

$f(x) = x^3 - 1$이 $x - 1$로 나누어떨어지는지 봅니다. $f(1) = 1 - 1 = 0$이므로 인수정리에 의해 $f(x)$는 $x - 1$로 나누어떨어집니다. 실제로 $x^3 - 1 = (x - 1)(x^2 + x + 1)$입니다.

## 관련 개념

- [다항식의 나눗셈](docs/concepts/algebra/high-1/다항식/나눗셈_정리.md)
- [다항식 나머지 정리](docs/concepts/algebra/high-1/다항식/나머지_정리.md)
- [다항식의 근](docs/concepts/algebra/high-1/다항식/다항식의_근.md)
