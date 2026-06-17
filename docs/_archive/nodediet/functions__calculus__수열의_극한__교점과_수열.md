---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/수열의_극한.md]
enables: []
mastery: unknown
---

# 교점과 수열

## 정확한 진술

함수 $f(x)$에 대해 방정식 $x = f(x)$의 해를 찾으려고 합니다. 이를 위해 다음과 같이 정의된 수열을 고려할 수 있습니다:

$$a_{n+1} = f(a_n), \quad n = 1, 2, 3, \ldots$$

초기값 $a_1$을 정하고 이 규칙에 따라 계속 계산하면, 적절한 조건 아래에서 수열 $\{a_n\}$은 방정식 $x = f(x)$의 해 $\alpha$로 수렴합니다. 이때 $\alpha = f(\alpha)$를 만족하는 값 $\alpha$를 함수 $f$의 고정점이라 부릅니다.

## 직관/기하적 의미

좌표평면에서 이 상황을 그려보면 과정이 명확해집니다. 곡선 $y = f(x)$ 위의 점 $(a_n, f(a_n))$에서 시작하여, 수평으로 직선 $y = x$로 이동합니다. 만나는 점의 좌표는 $(f(a_n), f(a_n))$이고, 여기서의 $x$좌표 $f(a_n)$이 다음 항 $a_{n+1}$이 됩니다. 그 후 수직으로 다시 곡선까지 올라가 같은 과정을 반복합니다. 이러한 지그재그 움직임을 통해 수열이 두 그래프의 교점으로 점점 가까워지는 것을 볼 수 있습니다.

## 한 줄 예

초기값 $a_1 = 2$에서 시작하여 $a_{n+1} = \frac{1}{2}a_n + 1$로 정의하면 (즉, $f(x) = \frac{1}{2}x + 1$), 수열이 직선 $y = \frac{1}{2}x + 1$과 $y = x$의 교점인 $(2, 2)$로 수렴합니다. `sympy.solve(x - (x/2 + 1), x)` → $[2]$
