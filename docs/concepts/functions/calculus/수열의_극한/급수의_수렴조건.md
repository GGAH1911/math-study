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

# 급수의 수렴조건

## 정확한 진술

수열 $\{a_n\}$의 **급수(series)** $\sum_{n=1}^{\infty} a_n$이 **수렴한다**는 것은, 부분합 수열 $S_N = \sum_{n=1}^{N} a_n$이 어떤 유한한 값 $L$에 수렴하는 것을 의미합니다. 즉,

$$\lim_{N \to \infty} S_N = \lim_{N \to \infty} \sum_{n=1}^{N} a_n = L$$

일 때 급수는 $L$로 수렴한다고 하며, 이때 $L$을 급수의 합이라 부릅니다. 부분합이 수렴하지 않으면 급수는 **발산**합니다.

## 직관/기하적 의미

무한개의 항을 모두 더한다는 개념은 직관적으로 말이 안 되지만, "계속 더해갈 때 어떤 값에 가까워지는가"를 부분합의 극한으로 정의함으로써 수학적으로 엄밀하게 만들 수 있습니다. 예를 들어 $0.9 + 0.09 + 0.009 + \cdots$를 "계속 더하면 1에 가까워진다"는 직관을 정확히 표현하는 것이 바로 급수의 수렴입니다. 부분합 $S_N = 0.999\cdots9$ (9가 $N$개)는 $N$이 커질수록 1에 가까워집니다.

## 한 줄 예

기하급수 $\sum_{n=1}^{\infty} \left(\frac{1}{2}\right)^n$은 부분합이 $S_N = 1 - \frac{1}{2^N} \to 1$이므로 1로 수렴합니다.

**참고:** 급수가 수렴하기 위한 **필요조건**은 $\lim_{n \to \infty} a_n = 0$입니다. 즉, 일반항이 0으로 수렴하지 않으면 급수는 절대 수렴할 수 없습니다. (예: $\sum_{n=1}^{\infty} n$은 발산)
