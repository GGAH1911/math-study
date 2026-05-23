---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/수열의_극한.md]
enables: []
mastery: unknown
---

# 무한급수의 합

수열의 모든 항을 더한 무한합의 값으로, 부분합의 극한으로 정의됩니다. 미적분 수열의 극한 단원의 핵심 개념입니다.

## 정의

수열 $\{a_n\}$에 대하여 부분합 $S_n = a_1 + a_2 + \cdots + a_n$이라 할 때, 극한 $\displaystyle\lim_{n \to \infty} S_n$이 일정한 값 $S$에 수렴하면 무한급수 $\displaystyle\sum_{n=1}^{\infty} a_n$이 **수렴**하고 그 **합**은 $S$입니다. 발산하면 합은 정의되지 않습니다.

특히 첫째항 $a$, 공비 $r$인 등비수열의 무한급수는 $|r| < 1$일 때 수렴하며 그 합은
$$\sum_{n=1}^{\infty} ar^{n-1} = \frac{a}{1 - r}.$$

## 예시

무한등비급수 $1 + \dfrac{1}{2} + \dfrac{1}{4} + \dfrac{1}{8} + \cdots$의 합을 구해 봅니다. 첫째항 $a = 1$, 공비 $r = \dfrac{1}{2}$로 $|r| < 1$이므로
$$\sum_{n=0}^{\infty} \left(\frac{1}{2}\right)^n = \frac{1}{1 - \frac{1}{2}} = 2.$$

또한 부분분수 분해를 활용한 $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n(n+1)}$은 $\dfrac{1}{n(n+1)} = \dfrac{1}{n} - \dfrac{1}{n+1}$로 망원합이 되어 $S_n = 1 - \dfrac{1}{n+1} \to 1$, 합은 $1$.

## 관련 개념

- [수열의 극한](docs/concepts/functions/calculus/수열의_극한.md)
