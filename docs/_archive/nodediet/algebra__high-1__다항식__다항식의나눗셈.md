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

# 다항식의 나눗셈

한 다항식을 다른 다항식으로 나누어 몫과 나머지를 구하는 연산입니다. 정수의 나눗셈과 비슷한 구조를 가지며, 고1 다항식 단원의 중심 연산입니다.

## 정의

두 다항식 $f(x)$와 $g(x)$ ($g(x) \neq 0$)에 대하여 다음을 만족시키는 다항식 $Q(x)$와 $R(x)$가 유일하게 존재합니다:
$$f(x) = g(x)\, Q(x) + R(x), \qquad \deg R(x) < \deg g(x).$$
여기서 $Q(x)$를 **몫**, $R(x)$를 **나머지**라 합니다. $R(x) = 0$이면 $f(x)$는 $g(x)$로 나누어떨어진다고 합니다.

## 예시

$f(x) = x^3 + 2x^2 - x + 5$를 $g(x) = x + 1$로 나누어 봅니다. 조립제법 또는 직접 나눗셈으로
$$x^3 + 2x^2 - x + 5 = (x+1)(x^2 + x - 2) + 7$$
을 얻습니다. 따라서 몫은 $x^2 + x - 2$, 나머지는 $7$입니다. 실제로 나머지 정리에 의해 $f(-1) = -1 + 2 + 1 + 5 = 7$로 일치합니다.

## 관련 개념

- [다항식 나머지 정리](docs/concepts/algebra/high-1/다항식/나머지_정리.md)
- [나누어떨어짐](docs/concepts/algebra/high-1/다항식/나누어떨어짐.md)
- [다항식](docs/concepts/algebra/high-1/다항식.md)
