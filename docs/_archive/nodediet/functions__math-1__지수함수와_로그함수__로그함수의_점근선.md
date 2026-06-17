---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/지수함수와_로그함수.md]
enables: []
mastery: unknown
---

# 로그함수의 점근선

## 정확한 진술

로그함수 $y = \log_a x$ (단, $a > 0, a \neq 1$)의 **점근선**은 수직선 $x = 0$ (y축)입니다. 이는 다음을 의미합니다:
- $x \to 0^+$일 때, $a > 1$이면 $y \to -\infty$
- $x \to 0^+$일 때, $0 < a < 1$이면 $y \to +\infty$

즉, 함수의 그래프가 y축에 무한히 가까워지지만 절대 만나지 않습니다.

## 직관 및 기하적 의미

로그함수는 지수함수의 역함수이므로, 두 함수의 점근선은 직선 $y = x$에 대해 대칭입니다.
- **지수함수** $y = a^x$의 수평 점근선: $y = 0$ (x축)
- **로그함수** $y = \log_a x$의 수직 점근선: $x = 0$ (y축)

정의역이 $x > 0$으로 제한되므로, $x$가 0에 가까워질수록 함수값은 한계 없이 커지거나 작아집니다. 이를 "점근선에 무한히 접근한다"고 표현합니다. 그래프는 y축 근처에서 가파르게 상승(또는 하강)합니다.

## 예시

**$y = \log_2 x$:** $x \to 0^+$일 때 $y \to -\infty$이므로, 점근선은 $x = 0$입니다.

**$y = \log_{1/2} x$:** $x \to 0^+$일 때 $y \to +\infty$이므로, 역시 점근선은 $x = 0$입니다.

두 경우 모두 정의역은 $x > 0$이고, y축이 점근선이 됩니다.

```python
# sympy를 이용한 극한 확인
from sympy import *
x = symbols('x', positive=True)
limit(log(x, 2), x, 0, '+')  # log_2(x)의 우극한 → -∞
limit(log(x, Rational(1,2)), x, 0, '+')  # log_{1/2}(x)의 우극한 → +∞
```
