---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/적분.md]
enables: []
mastery: unknown
---

# 분간함수

## 정확한 진술

함수 $f(x)$에 대해, 도함수가 $f(x)$가 되는 함수 $F(x)$를 **원시함수**(antiderivative)라 합니다. 즉, 다음을 만족합니다:

$$F'(x) = f(x)$$

$f(x)$의 원시함수가 존재하면, 모든 원시함수는 $F(x) + C$ 형태입니다. 여기서 $C$는 임의의 상수(적분상수)이며, 이를 기호로 $\displaystyle \int f(x) \, dx = F(x) + C$로 나타냅니다.

## 직관적 의미

원시함수는 **미분의 역연산**입니다. 어떤 함수를 미분했을 때 $f(x)$가 나왔다면, 그 원래 함수가 원시함수입니다.

기하학적으로는 $f(x)$의 그래프 아래 넓이를 구간 $[a, x]$에서 누적한 값이 원시함수가 됩니다(정적분과의 관계). 또한 $y = F(x)$ 그래프 위의 각 점에서 접선의 기울기가 정확히 $f(x)$ 값입니다.

## 한 줄 예

$f(x) = 3x^2$이면 $F(x) = x^3 + C$는 원시함수입니다. (왜냐하면 $(x^3 + C)' = 3x^2$)

**검증**: `sympy.diff(x**3 + 5, x)` → $3x^2$ ✓
