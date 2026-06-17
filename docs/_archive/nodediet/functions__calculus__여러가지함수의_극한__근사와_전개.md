---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md]
enables: []
mastery: unknown
---

# 근사와 전개

## 정확한 진술

어떤 함수 $f(x)$를 **근사(approximation)**한다는 것은, $x$가 특정 점 $a$ 근처에서 $f(x)$의 값을 더 간단한 함수로 대체하는 것입니다. 가장 중요한 근사 방법이 **Taylor 전개**로, 점 $a$에서 미분가능한 함수 $f(x)$를 다음과 같이 다항식으로 표현합니다:

$$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \frac{f'''(a)}{3!}(x-a)^3 + \cdots$$

$n$차까지만 취한 **$n$차 Taylor 근사식**은:

$$f(x) \approx f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x-a)^n$$

$a=0$일 때를 **Maclaurin 전개**라고 부르며, 많은 기본 함수들이 깔끔한 형태를 가집니다.

## 직관/기하적 의미

어떤 함수의 값을 정확히 계산하기 어려울 때, 그 함수가 특정 점 근처에서 어떤 다항식과 거의 같다면, 다항식으로 대체해 계산하는 것이 핵심입니다. 

**1차 근사**(일차함수)는 함수의 접선 방정식이므로, $x=a$ 근처에서 $f(x) \approx f(a) + f'(a)(x-a)$로 근사합니다. 

**2차 근사**는 포물선을 더하면서 곡률(concavity)까지 맞추고, 차수를 높일수록 더 넓은 범위에서 정확합니다. 이를 "**전개**"라 부르는 이유는 원래의 복잡한 함수를 항별로 풀어서 정보를 담기 때문입니다.

## 한 줄 예

$\sin x$의 $x=0$ 근처 3차 Taylor 전개: $\sin x \approx x - \frac{x^3}{6}$ (실제로 $\sin(0.5) \approx 0.479 \cdots$와 근사식 $0.5 - \frac{0.125}{6} \approx 0.479$가 거의 일치)

```python
# sympy로 검증
import sympy as sp
x = sp.Symbol('x')
sp.series(sp.sin(x), x, 0, 4)  # x에 대해 0 근처, 4차까지
```
