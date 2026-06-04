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

# 무한수열의 극한

## 정확한 진술

수열 $\{a_n\}$이 $n \to \infty$일 때 **극한값(극한) $L$로 수렴한다**는 것은 다음의 엄밀한 조건을 만족하는 것을 의미합니다:

임의의 양수 $\epsilon > 0$에 대하여, 어떤 자연수 $N$이 존재해서 $n > N$인 모든 자연수 $n$에 대해 $|a_n - L| < \epsilon$이 성립한다.

이를 기호로는 $\displaystyle \lim_{n \to \infty} a_n = L$ 또는 $a_n \to L$ $(n \to \infty)$로 나타낸다. 극한값이 존재하는 수열을 **수렴수열**, 존재하지 않으면 **발산수열**이라 부른다.

## 직관/기하적 의미

엄밀한 정의를 직관적으로 이해하면: "충분히 큰 $n$부터는 수열의 항들이 $L$에 얼마나 가깝든지(즉, $\epsilon$가 아무리 작아도) 그 거리 범위 내에 모두 들어간다"는 뜻입니다.

수직선 위에서 생각해보면, 점 $L$을 중심으로 반경 $\epsilon$인 열린 구간 $(L - \epsilon, L + \epsilon)$ 안에 어느 항부터는 계속 들어가는 모습을 상상할 수 있습니다. 아무리 $\epsilon$를 줄여서 구간을 좁혀도, 항상 충분히 큰 $n$부터는 모든 항 $a_n$이 그 구간 안에 있다는 것입니다. 이것이 극한으로 수렴한다는 기하학적 의미입니다.

## 한 줄 예

$a_n = \dfrac{1}{n}$일 때, $\displaystyle \lim_{n \to \infty} a_n = 0$이다. ($\epsilon = 0.01$이면 $N = 100$으로 잡으면 되므로 $n > 100$일 때 항상 $|a_n - 0| < 0.01$)
