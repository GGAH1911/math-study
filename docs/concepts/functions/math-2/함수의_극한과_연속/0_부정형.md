---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/함수의_극한과_연속.md]
enables: []
mastery: unknown
---

# 0/0 부정형

분자와 분모가 동시에 $0$으로 가는 극한 식의 부정형입니다. 수학2 함수의 극한 단원에서 식 변형이 필요한 핵심 유형입니다.

## 정의

극한 $\displaystyle\lim_{x \to a} \dfrac{f(x)}{g(x)}$에서 $\displaystyle\lim_{x \to a} f(x) = 0$이고 $\displaystyle\lim_{x \to a} g(x) = 0$일 때 이 극한을 **$\frac{0}{0}$ 부정형**이라 부릅니다. 직접 대입으로는 값이 결정되지 않으며, 다음 기법으로 식을 변형해 결정합니다.
- 다항식인 경우: 인수분해 후 공통인수 약분.
- 무리식인 경우: 켤레식을 곱해 유리화.
- 절댓값·분수식: 좌극한·우극한으로 나누어 봄.

## 예시

$\displaystyle\lim_{x \to 1} \dfrac{x^2 - 1}{x - 1}$을 계산해 봅니다. 분자를 인수분해하면
$$\frac{x^2 - 1}{x - 1} = \frac{(x-1)(x+1)}{x-1} = x + 1 \quad (x \neq 1).$$
따라서 극한값은 $\displaystyle\lim_{x \to 1} (x+1) = 2$입니다.

또한 $\displaystyle\lim_{x \to 0} \dfrac{\sqrt{x+4} - 2}{x}$는 켤레식을 곱해
$$\frac{(x+4) - 4}{x(\sqrt{x+4} + 2)} = \frac{1}{\sqrt{x+4} + 2} \to \frac{1}{4}.$$

## 관련 개념

- [극한값의 정의](docs/concepts/functions/math-2/함수의_극한과_연속/함수의_극한.md)
- [함수의 극한과 연속](docs/concepts/functions/math-2/함수의_극한과_연속.md)
