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

# 분할함수의 연속성

## 정확한 진술

분할함수(piecewise function)는 정의역을 여러 구간으로 나누어 각 구간에서 서로 다른 식으로 정의된 함수입니다. 다음과 같이 표현됩니다:

$$f(x) = \begin{cases} f_1(x) & \text{if } x \in D_1 \\ f_2(x) & \text{if } x \in D_2 \\ \vdots \end{cases}$$

**분할함수가 점 $x=a$에서 연속이려면:**
- $\lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = f(a)$ (좌극한 = 우극한 = 함숫값)

각 구간의 내부에서는 해당 식이 연속함수이면 자동으로 연속이므로, **경계점(구간이 나뉘는 지점)**에서만 연속성을 확인하면 됩니다.

## 직관/기하적 의미

분할함수의 그래프는 여러 곡선이나 직선으로 이루어집니다. 경계점에서는 "점프"나 "끊김"이 생길 수 있습니다. 그래프가 경계점에서 끊어지지 않고 매끄럽게 이어지려면, 좌쪽에서 다가오는 극한값과 우쪽에서 다가오는 극한값이 그 점에서의 함숫값과 모두 같아야 합니다. 이것이 바로 연속의 정의입니다.

## 한 줄 예

$$f(x) = \begin{cases} x^2 & \text{if } x < 1 \\ 3-x & \text{if } x \geq 1 \end{cases}$$

$x=1$에서: $\lim_{x \to 1^-} f(x) = 1$, $\lim_{x \to 1^+} f(x) = 3-1 = 2$, $f(1) = 2$이므로 좌극한 ≠ 우극한 → **불연속**.

반면 $f(x) = \begin{cases} x+1 & \text{if } x < 2 \\ 3 & \text{if } x \geq 2 \end{cases}$는 $x=2$에서 $\lim_{x \to 2^-} f(x) = 3 = f(2)$이므로 **연속** (`sympy.limit((x+1), x, 2, '-')` = 3).
