---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md, docs/concepts/functions/calculus/여러가지함수의_미분.md]
enables: []
mastery: unknown
auto_explained: true
---

# Taylor 근사

함수 $f(x)$가 $x = a$ 근방에서 미분가능할 때, $x$가 $a$에 매우 가까우면 함수값 $f(x)$를 간단한 다항식으로 근사할 수 있다. 이를 **Taylor 근사**라 한다.

가장 기본적인 형태는 **1차 Taylor 근사**로, 접선을 이용한다.

$$f(x) \approx f(a) + f'(a)(x - a)$$

이 식은 $x = a$ 근방에서 $f(x)$의 값을 접선의 $y$값으로 대체하는 것이다. $x - a$를 $h$로 쓰면 $f(a+h) \approx f(a) + f'(a)h$로도 표현한다.

2차항까지 포함한 **2차 Taylor 근사**는 다음과 같다.

$$f(x) \approx f(a) + f'(a)(x-a) + \frac{f''(a)}{2}(x-a)^2$$

근사의 핵심은 **$x$가 $a$에 가까울수록** 오차가 작아진다는 점이다. $x$와 $a$의 차이가 충분히 작으면, 복잡한 함수 $f(x)$를 이 다항식으로 사실상 같은 값으로 다룰 수 있다.

## 예시

**예시 1.** $f(x) = \sin x$를 $x = 0$ 근방에서 1차 Taylor 근사하라.

$f(0) = \sin 0 = 0$, $f'(x) = \cos x$이므로 $f'(0) = 1$이다. 따라서

$$\sin x \approx 0 + 1 \cdot (x - 0) = x$$

실제로 $x = 0.1$이면 $\sin 0.1 \approx 0.0998\ldots$이고, 근사값은 $0.1$로 오차가 매우 작다.

**예시 2.** $f(x) = e^x$를 $x = 0$ 근방에서 2차 Taylor 근사하라.

$f(0) = 1$, $f'(0) = 1$, $f''(0) = 1$이므로

$$e^x \approx 1 + x + \frac{x^2}{2}$$

$x = 0.2$를 대입하면 근사값은 $1 + 0.2 + 0.02 = 1.22$이고, 실제 $e^{0.2} \approx 1.2214\ldots$와 매우 가깝다.

## 관련 개념

**여러가지함수의 극한**은 Taylor 근사의 바탕이 된다. $x \to a$일 때 $f(x)$가 특정 값에 수렴한다는 사실이 있어야 근사가 의미를 가진다. 특히 $\lim_{x \to 0} \dfrac{\sin x}{x} = 1$이라는 극한은 $\sin x \approx x$라는 1차 근사를 그대로 표현한 것이다.

**여러가지함수의 미분**에서 배운 $\sin x$, $\cos x$, $e^x$, $\ln x$ 등의 도함수가 Taylor 근사 계수를 직접 결정한다. 미분을 모르면 근사식을 세울 수 없으므로, 미분은 Taylor 근사의 필수 선수 개념이다.

이웃한 개념으로는 **미분과 선형근사**가 있다. 1차 Taylor 근사는 곧 접선에 의한 선형근사이며, $\Delta y \approx f'(a)\,\Delta x$라는 미분의 활용과 동일한 내용이다. 또한 **함수의 극값 판정**과도 연결된다. 2차 Taylor 근사에서 $f'(a) = 0$이면 $f''(a)$의 부호가 극소·극대를 결정하는 원리가 그대로 담겨 있다.
