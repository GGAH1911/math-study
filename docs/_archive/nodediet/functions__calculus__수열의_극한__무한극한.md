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

# 무한극한

## 정확한 진술

수열 $\{a_n\}$이 **무한극한** $L$을 가진다는 것은 다음을 의미합니다: 아무리 작은 양수 $\varepsilon > 0$이 주어지더라도, 어떤 자연수 $N$이 존재하여 $n > N$인 모든 자연수 $n$에 대해 $|a_n - L| < \varepsilon$이 성립한다는 뜻입니다. 

이를 기호로 나타내면 $\lim_{n \to \infty} a_n = L$ 또는 $n \to \infty$일 때 $a_n \to L$입니다.

## 직관과 기하적 의미

무한극한은 수열의 항들이 $n$이 커질수록 특정 값 $L$에 **얼마든지 가깝게** 모인다는 의미입니다. "얼마든지 가깝게"라는 것은 기준(오차한계)을 $\varepsilon$으로 아무리 작게 잡더라도, 어느 항부터는 그 기준 이내에 들어간다는 뜻입니다.

기하적으로 보면, 직선 $y = L$을 중심으로 폭이 $2\varepsilon$인 띠 모양 구간을 그렸을 때, 충분히 큰 $n$부터는 모든 점 $(n, a_n)$이 이 띠 안에 들어가게 됩니다. 그 "충분히 큰 $n$"의 기준이 $N$입니다.

## 한 줄 예

$a_n = \frac{1}{n}$이면 $\lim_{n \to \infty} a_n = 0$입니다. 왜냐하면 아무리 작은 $\varepsilon > 0$에 대해서도 $N = \lceil \frac{1}{\varepsilon} \rceil$로 잡으면, $n > N$일 때 $|a_n - 0| = \frac{1}{n} < \frac{1}{N} \leq \varepsilon$이기 때문입니다. 예를 들어 $\varepsilon = 0.01$이면 $N = 100$부터 모든 항이 $-0.01$과 $0.01$ 사이에 있습니다. (`from sympy import *; n = symbols('n'); limit(1/n, n, oo)`)
