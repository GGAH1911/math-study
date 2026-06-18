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

# 좌극한과 우극한

## 정확한 진술

함수 $f(x)$에서 점 $a$로의 **좌극한**(left-hand limit)은 $x$가 $a$보다 작으면서 $a$에 가까워질 때 $f(x)$가 접근하는 값이며, $\lim_{x \to a^-} f(x)$로 표기합니다. 마찬가지로 **우극한**(right-hand limit)은 $x$가 $a$보다 크면서 $a$에 가까워질 때 $f(x)$가 접근하는 값이며, $\lim_{x \to a^+} f(x)$로 표기합니다.

형식적으로:
- $\lim_{x \to a^-} f(x) = L$ : 임의의 양수 $\varepsilon$에 대해, $\delta > 0$가 존재하여 $a - \delta < x < a$이면 $|f(x) - L| < \varepsilon$
- $\lim_{x \to a^+} f(x) = L$ : 임의의 양수 $\varepsilon$에 대해, $\delta > 0$가 존재하여 $a < x < a + \delta$이면 $|f(x) - L| < \varepsilon$

## 직관과 기하적 의미

그래프 위에서 점 $a$에 접근할 때, **왼쪽에서만** 접근하는 경우와 **오른쪽에서만** 접근하는 경우를 구분합니다. 극한값은 함수가 점 $a$에서 어떤 값을 갖는지와는 무관하게, 한 방향으로만 접근했을 때 함수값이 수렴하는 값입니다.

중요한 성질: **$f(x)$가 점 $a$에서 극한값을 가지려면 좌극한과 우극한이 존재하고 서로 같아야 합니다.** 즉, $\lim_{x \to a} f(x) = L$ $\Leftrightarrow$ $\lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = L$

## 한 줄 예

$f(x) = \begin{cases} x+1 & (x < 2) \\ 5 & (x = 2) \\ 3x-1 & (x > 2) \end{cases}$일 때:

- 좌극한: $\lim_{x \to 2^-} f(x) = 2 + 1 = 3$ (왼쪽에서 $y = x+1$을 따라 접근)
- 우극한: $\lim_{x \to 2^+} f(x) = 3(2) - 1 = 5$ (오른쪽에서 $y = 3x-1$을 따라 접근)
- 함수값: $f(2) = 5$

좌극한과 우극한이 다르므로 ($3 \neq 5$), $x = 2$에서 극한이 존재하지 않습니다. 이런 불연속점을 **점프 불연속**(jump discontinuity)이라 부릅니다.
