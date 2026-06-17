---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/수열.md]
enables: []
mastery: unknown
---

# 반복 기하 구성

## 정확한 진술
반복 기하 구성(iterative geometric construction)은 기본 도형에서 시작하여 일정한 규칙을 반복적으로 적용하여 도형을 단계적으로 만드는 과정입니다. $n$단계 도형을 $G_n$이라 하면, $G_{n+1}$은 $G_n$의 각 부분에 동일한 기하학적 변환을 적용하여 만들어집니다. 극한값 $\lim_{n \to \infty} G_n$이 최종 도형(극한 도형)입니다.

## 직관과 기하적 의미
반복 기하 구성은 **단순한 규칙의 무한 반복으로 복잡한 도형을 만드는 방법**입니다. 각 단계에서 도형의 일부가 축소되거나 제거되면서, 전체 도형과 그 부분이 닮음 관계를 유지합니다(자기유사성). 이 특징이 반복 구성 도형의 본질이며, 이런 도형들을 프랙탈(fractal)이라 부릅니다. 단계가 진행될수록 도형의 형태는 더욱 정교해지지만, 수열의 극한으로 그 넓이나 둘레 같은 성질을 정확히 계산할 수 있습니다.

## 구체적 예시
**시에르핀스키 삼각형**: 정삼각형에서 출발하여, 매 단계마다 남은 도형의 가운데 삼각형을 제거합니다.

- $G_0$: 넓이 = $A$ (정삼각형)
- $G_1$: 중심 삼각형(크기 $\frac{1}{4}$)제거 → 넓이 = $\frac{3}{4}A$
- $G_n$: 넓이 = $A \times \left(\frac{3}{4}\right)^n$

극한에서 $\lim_{n \to \infty} A \times \left(\frac{3}{4}\right)^n = 0$이므로 넓이는 0이 되지만, 둘레의 길이는 무한으로 증가합니다. (`import sympy as sp; n = sp.Symbol('n'); sp.limit(3**(1/sp.Rational(2,4))**n, n, sp.oo)` → 무한)
