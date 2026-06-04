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

# 급수의수렴

## 정확한 진술

급수 $\sum_{n=1}^{\infty} a_n$이 **수렴한다**는 것은, 부분합 수열 $S_N = \sum_{n=1}^{N} a_n$ (처음 $N$개 항의 합)이 어떤 실수 $S$로 수렴할 때를 말합니다. 즉,

$$\lim_{N \to \infty} S_N = S$$

이면 이 급수는 $S$로 수렴한다고 하고, $\displaystyle\sum_{n=1}^{\infty} a_n = S$로 나타냅니다. 반대로 부분합 수열이 수렴하지 않으면 급수는 **발산**합니다.

## 직관/기하적 의미

무한히 많은 항을 더했을 때, 그 합이 어떤 한정된 값에 도달할 수 있다는 의미입니다. 예를 들어 $a_n$이 0으로 빠르게 수렴하는 수열이면, 각 항을 계속 더해도 합이 어느 값 근처에서 머물게 됩니다. 수열의 극한이 "한 점으로 수렴하는 현상"이라면, 급수의 수렴은 "누적된 합이 한 점으로 수렴하는 현상"입니다.

## 한 줄 예

무한등비급수 $\displaystyle\sum_{n=1}^{\infty} \frac{1}{2^n} = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \cdots$는 부분합이 $S_N = 1 - \frac{1}{2^N}$이고, $N \to \infty$일 때 $S_N \to 1$이므로 1로 수렴합니다. (검산: `sum(Rational(1, 2**n) for n in range(1, 100))` ≈ 0.99999...)
