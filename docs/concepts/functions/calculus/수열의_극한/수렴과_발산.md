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

# 수렴과 발산

## 정확한 진술

수열 $\{a_n\}$이 **수렴한다**는 것은, 어떤 실수 $L$이 존재하여 다음을 만족하는 경우입니다:

임의의 양수 $\varepsilon$에 대하여, 어떤 자연수 $N$이 존재하여 $n \geq N$일 때 항상 $|a_n - L| < \varepsilon$이다.

이때 $L$을 수열의 **극한값**이라 하고, $\lim_{n \to \infty} a_n = L$ 또는 $a_n \to L$로 표기합니다. 어떤 실수로도 수렴하지 않는 수열을 **발산한다**고 합니다.

## 직관 및 기하적 의미

$\varepsilon$은 "허용 오차"입니다. 아무리 작은 오차 범위를 정하더라도, $n$이 충분히 크기만 하면 모든 항이 극한값 주변 $(L - \varepsilon, L + \varepsilon)$ 안에 들어온다는 뜻이 수렴입니다.

수열을 점열 $(n, a_n)$으로 생각하면, 수렴은 이 점들이 수평선 $y = L$ 위아래로 점점 가까워지며 들어오는 현상입니다. 반면 발산은 일정한 값으로 모아지지 않고 진동하거나 무한히 커지거나 내려가는 경우입니다.

## 예

- $a_n = \frac{1}{n}$는 $0$으로 수렴: $\lim_{n \to \infty} \frac{1}{n} = 0$
- $a_n = 2$ (상수 수열)는 $2$로 수렴
- $a_n = (-1)^n$은 $-1, 1, -1, 1, \ldots$로 진동하므로 발산
- $a_n = n$은 무한히 커져 발산

SymPy 검산: `from sympy import limit, oo, n as n_var; limit(1/n_var, n_var, oo)` → `0`
