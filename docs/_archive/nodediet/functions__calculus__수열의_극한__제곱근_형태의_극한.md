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

# 제곱근 형태의 극한

## 정확한 진술

제곱근 형태의 극한이란 수열의 일반항이 제곱근을 포함하고 있을 때, 그 수열의 극한값을 구하는 문제를 말합니다. 특히 다음과 같은 형태들이 자주 다뤄집니다:

- $\lim_{n\to\infty} \sqrt{n^2 + an + b} - n$ (유리화를 통한 계산)
- $\lim_{n\to\infty} \sqrt{an^2 + bn + c} - \sqrt{dn^2 + en + f}$ (분자의 유리화)
- $\lim_{n\to\infty} \sqrt{f(n)}$ (직접 계산)

이러한 극한값을 구할 때는 보통 식을 유리화하거나, 분자와 분모를 최고차항으로 인수분해하는 방법을 사용합니다.

## 직관/기하적 의미

제곱근이 포함된 수열에서 극한을 구할 때 가장 흔한 어려움은 $\infty - \infty$ 꼴의 부정형입니다. 예를 들어 $\sqrt{n^2 + n} - n$처럼 보이면 두 항이 모두 무한대로 발산하므로 직접 계산할 수 없습니다. 이때 **유리화**(켤레를 곱해서 분모에 둔다)를 사용하면 제곱근을 없애고 정확한 극한값을 찾을 수 있습니다. 기하학적으로는 함수 그래프에서 $n$이 커질수록 $\sqrt{n^2 + n}$이 $n$에 점점 가까워지되, 그 "차이"가 일정한 수에 수렴하는 모습으로 이해할 수 있습니다.

## 한 줄 예

$\lim_{n\to\infty} (\sqrt{n^2 + 2n} - n)$을 구하려면 켤레를 곱해 유리화합니다:

$$\lim_{n\to\infty} \frac{(\sqrt{n^2+2n}-n)(\sqrt{n^2+2n}+n)}{\sqrt{n^2+2n}+n} = \lim_{n\to\infty} \frac{2n}{\sqrt{n^2+2n}+n} = \lim_{n\to\infty} \frac{2}{\sqrt{1+\frac{2}{n}}+1} = 1$$

(`sympy.limit(sqrt(n**2 + 2*n) - n, n, oo)` → 결과: $1$)
