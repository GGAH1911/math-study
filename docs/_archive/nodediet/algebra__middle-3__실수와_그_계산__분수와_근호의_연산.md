---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 중3
prerequisites: [docs/concepts/algebra/middle-3/실수와_그_계산.md]
enables: []
mastery: unknown
---

# 분수와 근호의 연산

## 정확한 진술

분수와 근호의 연산이란, 분수(분자와 분모로 이루어진 유리수)와 근호(제곱근, 세제곱근 등의 무리수)가 포함된 식을 더하고, 빼고, 곱하고, 나누는 모든 계산 규칙을 말합니다. 구체적으로는:

- **분수 간의 연산**: $\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}$, $\frac{a}{b} \times \frac{c}{d} = \frac{ac}{bd}$
- **근호 간의 연산**: $\sqrt{a} \times \sqrt{b} = \sqrt{ab}$ (단, $a, b \geq 0$), $\sqrt{a} + \sqrt{b}$는 $\sqrt{a}$와 $\sqrt{b}$가 같은 것일 때만 계산
- **분수와 근호의 혼합**: $\frac{1}{\sqrt{a}}$의 분모 유리화($= \frac{\sqrt{a}}{a}$) 등

## 직관/기하적 의미

분수는 "전체를 몇 등분하여 몇 개를 취한 것"이고, 근호는 "어떤 수를 제곱해서 안의 수가 되는 양수"를 나타냅니다. 이 둘을 함께 다루면 수학에서 나타나는 거의 모든 수를 표현할 수 있습니다. 예를 들어 정사각형의 대각선 길이 $\sqrt{2}$나, 원의 반지름을 여러 번 나눈 길이 같은 실제 크기들을 정확히 계산할 수 있게 해줍니다.

## 한 줄 예

$\frac{2}{\sqrt{3}} = \frac{2\sqrt{3}}{3}$ (분모를 유리화했으며, `sympy.simplify(2/sqrt(3))` 로 확인 가능)

또는 $\sqrt{12} + \sqrt{3} = 2\sqrt{3} + \sqrt{3} = 3\sqrt{3}$ (근호 안의 수를 간단히 한 후 같은 근호끼리 더함)
