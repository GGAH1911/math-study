---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/함수의_극한과_연속.md]
enables: []
mastery: unknown
---

# 부정형 계산

## 정확한 진술

극한 계산에서 함수의 극한값을 직접 대입했을 때 $\frac{0}{0}$, $\frac{\infty}{\infty}$, $0 \cdot \infty$, $\infty - \infty$, $0^0$, $1^\infty$, $\infty^0$ 등의 꼴이 나타나는 경우를 **부정형(indeterminate form)**이라 합니다. 이 경우 극한값이 유일하게 정해지지 않으므로, 추가적인 계산이나 변형이 필요합니다.

## 직관/기하적 의미

함수값을 직접 대입할 수 있다면(분모가 0이 아니면) 극한값은 함수값과 같습니다. 그러나 부정형은 이 방법으로 극한값을 바로 알 수 없는 상황입니다. 예를 들어 $\lim_{x \to 1} \frac{x^2 - 1}{x - 1}$에서 $x = 1$을 대입하면 $\frac{0}{0}$이 되는데, 이는 "극한값이 정해지지 않았다"는 뜻이 아니라 "분자와 분모가 동시에 0으로 수렴하고 있다"는 의미입니다. 따라서 분자·분모를 인수분해하거나 미분하는 등의 다른 방법으로 극한값을 구해야 합니다. 같은 부정형 $\frac{0}{0}$이라도 인수분해, 켤레식 곱셈, 로피탈의 정리 등 여러 경로가 있으며, 각각 다른 극한값을 가질 수 있습니다.

## 한 줄 예

$$\lim_{x \to 2} \frac{x^2 - 4}{x - 2} = \lim_{x \to 2} \frac{(x-2)(x+2)}{x-2} = \lim_{x \to 2} (x+2) = 4$$

$x = 2$를 대입하면 $\frac{0}{0}$(부정형)이지만, 인수분해를 통해 극한값은 4입니다.
