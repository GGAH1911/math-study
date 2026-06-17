---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md]
enables: []
mastery: unknown
---

# 0/0 꼴 극한

분자와 분모가 모두 $0$으로 수렴할 때 나타나는 부정형 극한입니다. 미적분 여러 가지 함수의 극한 단원에서 식 변형의 핵심 유형입니다.

## 정의

$\displaystyle\lim_{x \to a} \dfrac{f(x)}{g(x)}$에서 $\displaystyle\lim_{x \to a} f(x) = 0$이고 $\displaystyle\lim_{x \to a} g(x) = 0$인 경우를 **$\frac{0}{0}$ 꼴 부정형**이라 합니다. 직접 대입으로는 값이 결정되지 않으므로, 다음 기법으로 식을 변형해 결정합니다.
- 인수분해 후 약분.
- 분자·분모에 켤레식을 곱하여 유리화.
- 삼각함수의 기본 극한 $\displaystyle\lim_{x \to 0} \dfrac{\sin x}{x} = 1$ 등을 활용.

## 예시

$\displaystyle\lim_{x \to 2} \dfrac{x^2 - 4}{x - 2}$를 계산해 봅니다. 분자를 인수분해하면 $\dfrac{(x-2)(x+2)}{x-2} = x + 2$ ($x \neq 2$)이므로 극한값은 $\displaystyle\lim_{x \to 2} (x + 2) = 4$입니다.

또한 $\displaystyle\lim_{x \to 0} \dfrac{\sqrt{1+x} - 1}{x}$는 분자·분모에 $\sqrt{1+x} + 1$을 곱해 유리화하면
$$\frac{(1+x) - 1}{x(\sqrt{1+x} + 1)} = \frac{1}{\sqrt{1+x} + 1} \to \frac{1}{2}.$$

## 관련 개념

- [여러 가지 함수의 극한](docs/concepts/functions/calculus/여러가지함수의_극한.md)
