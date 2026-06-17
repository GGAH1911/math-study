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

# 무한대로의 극한

## 정확한 진술

수열 $\{a_n\}$이 무한대로 갈 때 극한값 $L$으로 수렴한다는 것은 다음을 의미합니다:

**$\lim_{n \to \infty} a_n = L$ ⟺ 임의의 양수 $\varepsilon > 0$에 대하여, 어떤 자연수 $N$이 존재하여 $n > N$이면 $|a_n - L| < \varepsilon$이다.**

다르게 표현하면, $n$이 충분히 크면 $a_n$을 $L$에 원하는 만큼 가깝게 만들 수 있다는 뜻입니다. 만약 이런 $L$이 존재하지 않으면 수열은 발산한다고 합니다.

## 직관과 기하적 의미

$\varepsilon$-$N$ 정의는 처음엔 낯설지만, 아이디어는 간단합니다. 수열의 극한은 "충분히 큰 $n$에 대해 모든 항이 $L$ 근처에 모여 있는가"를 확인하는 것입니다.

수직선 위에서 보면, $L$ 주변에 폭이 $2\varepsilon$인 띠 모양의 구간 $(L - \varepsilon, L + \varepsilon)$을 그렸을 때, 처음 유한 개 항들을 제외한 모든 항이 이 띠 안에 들어온다는 의미입니다. $\varepsilon$을 아무리 작게 (예: $0.001$) 잡아도 어떤 시점 이후의 모든 항이 그 띠 안에 있으면, 수열은 $L$로 수렴합니다.

## 한 줄 예

수열 $a_n = \frac{1}{n}$은 $n \to \infty$일 때 $0$으로 수렴합니다. 왜냐하면 아무리 작은 $\varepsilon > 0$을 주더라도, $N = \lceil 1/\varepsilon \rceil$로 잡으면 $n > N$일 때 $|1/n - 0| = 1/n < \varepsilon$이 성립하기 때문입니다. 

`from sympy import symbols, limit, oo; n = symbols('n'); limit(1/n, n, oo)` → 결과: `0`
