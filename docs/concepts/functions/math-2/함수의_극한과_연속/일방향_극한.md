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

# 일방향 극한

## 정확한 진술

함수 $f(x)$가 $a$를 포함하는 어떤 구간에서 정의되었을 때, **좌극한**(left-hand limit)과 **우극한**(right-hand limit)을 다음과 같이 정의합니다.

**좌극한**: $x$가 $a$보다 작은 쪽에서 $a$에 접근할 때, $f(x)$가 $L$에 수렴하면
$$\lim_{x \to a^-} f(x) = L$$

**우극한**: $x$가 $a$보다 큰 쪽에서 $a$에 접근할 때, $f(x)$가 $L$에 수렴하면
$$\lim_{x \to a^+} f(x) = L$$

정확한 정의는 다음과 같습니다: $\lim_{x \to a^-} f(x) = L$ ⟺ 임의의 $\varepsilon > 0$에 대해, $\delta > 0$이 존재하여 $a - \delta < x < a$일 때 $|f(x) - L| < \varepsilon$이 성립합니다.

## 직관과 기하적 의미

극한을 배울 때 $\lim_{x \to a} f(x)$는 $x$가 $a$에 가까워질 때 $f(x)$의 행동을 나타냅니다. 그런데 **함수가 $a$에서 불연속이거나, 특정 방향에서만 접근 가능한 경우**가 있습니다.

예를 들어 $f(x) = \lfloor x \rfloor$ (바닥 함수)는 정수에서 점프합니다. $x = 1$ 근처에서:
- 왼쪽에서 접근하면 (0.9, 0.99, 0.999, ...) $f(x) = 0$
- 오른쪽에서 접근하면 (1.1, 1.01, 1.001, ...) $f(x) = 1$

이렇게 **방향에 따라 다른 값으로 수렴할 수 있습니다**. 일방향 극한은 이러한 상황을 정확히 기술합니다.

**중요한 성질**: 양쪽 극한이 같아야만 $\lim_{x \to a} f(x)$가 존재합니다. 즉,
$$\lim_{x \to a} f(x) = L \iff \lim_{x \to a^-} f(x) = L \text{ and } \lim_{x \to a^+} f(x) = L$$

## 간단한 예

$$f(x) = \begin{cases} 2x & x < 1 \\ x + 1 & x \geq 1 \end{cases}$$

에서 $x \to 1$일 때:
- $\lim_{x \to 1^-} f(x) = 2(1) = 2$
- $\lim_{x \to 1^+} f(x) = 1 + 1 = 2$

따라서 $\lim_{x \to 1} f(x) = 2$입니다. (좌극한과 우극한이 같으므로)

```python
# sympy로 확인
from sympy import symbols, limit, Piecewise
x = symbols('x')
f = Piecewise((2*x, x < 1), (x + 1, x >= 1))
print(limit(f, x, 1, '-'), limit(f, x, 1, '+'))  # 2, 2
```
