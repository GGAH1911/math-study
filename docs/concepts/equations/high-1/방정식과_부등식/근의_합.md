---
unit: 방정식과 부등식
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 방정식
grade: 고1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# 근의 합

## 정확한 진술

이차방정식 $ax^2 + bx + c = 0$ (단, $a \neq 0$)의 두 근을 $\alpha, \beta$라 할 때, 두 근의 합은 다음과 같습니다:

$$\alpha + \beta = -\frac{b}{a}$$

이를 **근의 합**이라 부르며, 이는 근과 계수의 관계(비에타 정리)에서 나오는 가장 기본적인 성질입니다.

## 직관과 의미

이 관계식은 이차함수의 대칭성에서 비롯됩니다. 이차함수 $y = ax^2 + bx + c$의 그래프는 직선 $x = -\frac{b}{2a}$를 중심으로 대칭이며, 이 직선이 두 근의 **정확한 중점**을 지나갑니다. 따라서 두 근의 산술평균이 $-\frac{b}{2a}$이므로, 합은 자동으로 $-\frac{b}{a}$가 됩니다. 

다시 말해, 방정식의 계수 $b$는 두 근의 합에 대한 정보를 완전히 담고 있습니다. 근의 공식으로부터도 확인할 수 있습니다:

$$\alpha + \beta = \frac{-b + \sqrt{b^2-4ac}}{2a} + \frac{-b - \sqrt{b^2-4ac}}{2a} = \frac{-2b}{2a} = -\frac{b}{a}$$

## 간단한 예

방정식 $x^2 - 5x + 6 = 0$에서 $a=1, b=-5, c=6$이므로:
$$\alpha + \beta = -\frac{(-5)}{1} = 5$$

실제로 인수분해하면 $(x-2)(x-3) = 0$이므로 근은 $2, 3$이고, 합은 $2+3=5$입니다. (검증: `sympy.solve(x**2 - 5*x + 6, x)` → `[2, 3]`)
