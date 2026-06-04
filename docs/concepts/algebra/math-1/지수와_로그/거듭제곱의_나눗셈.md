---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 수학1
prerequisites: [docs/concepts/algebra/math-1/지수와_로그.md]
enables: []
mastery: unknown
---

# 거듭제곱의 나눗셈

## 정확한 진술

같은 밑을 가진 거듭제곱을 나눌 때는 밑은 그대로 두고 지수를 빼는 규칙입니다.

$a \neq 0$이고 $m, n$이 양의 정수일 때:
$$\frac{a^m}{a^n} = a^{m-n}$$

더 일반적으로는 지수가 음수인 경우까지 확장되어, $m < n$이면 결과가 음의 지수를 가집니다. 예를 들어 $\frac{a^2}{a^5} = a^{2-5} = a^{-3}$입니다.

## 직관과 의미

거듭제곱의 곱셈이 지수를 더하는 것과 반대로, 나눗셈은 지수를 빼는 것입니다. 왜 그럴까요?

$\frac{a^5}{a^3}$을 구체적으로 계산해봅시다.
$$\frac{a^5}{a^3} = \frac{a \times a \times a \times a \times a}{a \times a \times a}$$

분자와 분모에서 공통으로 나타나는 $a \times a \times a$을 약분하면:
$$= a \times a = a^2$$

지수로 표현하면 $5 - 3 = 2$이므로 $a^{5-3} = a^2$가 됩니다. 이것이 거듭제곱의 나눗셈 규칙의 본질입니다.

## 간단한 예

$\frac{2^7}{2^3} = 2^{7-3} = 2^4 = 16$

$\frac{3^5}{3^2} = 3^3 = 27$ (검산: $3^5 = 243$, $3^2 = 9$, $243 \div 9 = 27$ ✓)

지수 계산 검증: `2**7 // 2**3` → `16`, `3**5 // 3**2` → `27`
