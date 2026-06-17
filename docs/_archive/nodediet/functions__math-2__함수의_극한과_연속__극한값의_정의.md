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

# 극한값의 정의

함수의 입력이 어떤 값에 한없이 가까워질 때 함숫값이 한없이 가까워지는 값을 가리키는 개념입니다. 수학2 함수의 극한과 연속 단원의 출발점입니다.

## 정의

함수 $f(x)$에서 $x$가 $a$가 아니면서 $a$에 한없이 가까워질 때 $f(x)$의 값이 일정한 실수 $L$에 한없이 가까워지면, $L$을 $x \to a$에서의 $f(x)$의 **극한값**이라 하고
$$\lim_{x \to a} f(x) = L$$
로 씁니다. 좌극한 $\displaystyle\lim_{x \to a^-} f(x)$와 우극한 $\displaystyle\lim_{x \to a^+} f(x)$가 같은 값일 때에만 극한값이 존재합니다.

극한값은 $f(a)$ 값과는 별개이며, $f$가 $x = a$에서 정의되어 있지 않아도 극한값은 존재할 수 있습니다.

## 예시

$f(x) = \dfrac{x^2 - 1}{x - 1}$의 $x \to 1$에서의 극한을 봅니다. $f$는 $x = 1$에서 정의되지 않지만, $x \neq 1$일 때 $f(x) = x + 1$이므로 좌·우극한이 모두 $2$입니다. 따라서 $\displaystyle\lim_{x \to 1} f(x) = 2$.

또한 부호함수 $\mathrm{sgn}(x)$는 $x \to 0$의 좌극한이 $-1$, 우극한이 $1$로 서로 다르므로 $x \to 0$에서 극한값이 존재하지 않습니다.

## 관련 개념

- [0/0 부정형](docs/concepts/functions/math-2/함수의_극한과_연속/0_부정형.md)
- [함수의 연속](docs/concepts/functions/math-2/함수의_극한과_연속/연속함수.md)
- [함수의 극한과 연속](docs/concepts/functions/math-2/함수의_극한과_연속.md)
