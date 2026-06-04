---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 고1
prerequisites: [docs/concepts/algebra/high-1/다항식.md]
enables: []
mastery: unknown
---

# 다항식나눗셈

## 정확한 진술

다항식 $f(x)$를 다항식 $g(x)$ (단, $g(x) \neq 0$)로 나눌 때, **몫** $q(x)$와 **나머지** $r(x)$가 유일하게 존재합니다. 다항식 나눗셈의 핵심은 다음 항등식입니다:

$$f(x) = g(x) \cdot q(x) + r(x)$$

여기서 나머지 $r(x)$는 $g(x)$보다 차수가 작거나 ($\deg(r) < \deg(g)$) 영다항식입니다. $f(x)$를 **피제수**, $g(x)$를 **제수**, $q(x)$를 **몫**, $r(x)$를 **나머지**라 부릅니다.

## 직관·기하적 의미

정수의 나눗셈처럼 다항식도 나눗셈 규칙을 따릅니다. 예를 들어 $17 = 5 \times 3 + 2$처럼, $f(x) = g(x) \cdot q(x) + r(x)$입니다. 다항식 나눗셈은 보통 **긴 나눗셈**(long division) 또는 **조립제법**(synthetic division, 특히 일차식으로 나눌 때)으로 계산됩니다. 

나머지가 상수일 때, **나머지 정리**가 성립합니다: $f(x)$를 일차식 $x - a$로 나눈 나머지는 $f(a)$입니다. 이는 다항식 인수분해와 근 찾기에서 필수 도구입니다.

## 구체적 예

$f(x) = x^3 + 2x^2 - 5x + 3$을 $g(x) = x - 1$로 나누어봅시다.

긴 나눗셈으로 진행하면:
- $x^3 \div x = x^2$ → $x^2(x-1) = x^3 - x^2$ 빼기
- $3x^2 \div x = 3x$ → $3x(x-1) = 3x^2 - 3x$ 빼기  
- $-2x \div x = -2$ → $-2(x-1) = -2x + 2$ 빼기
- 나머지: $1$

따라서 $x^3 + 2x^2 - 5x + 3 = (x-1)(x^2 + 3x - 2) + 1$

또는 나머지 정리로: $f(1) = 1 + 2 - 5 + 3 = 1$ ✓

(`sympy.div(sympy.symbols('x')**3 + 2*sympy.symbols('x')**2 - 5*sympy.symbols('x') + 3, sympy.symbols('x') - 1)` → `(x^2 + 3x - 2, 1)`)
