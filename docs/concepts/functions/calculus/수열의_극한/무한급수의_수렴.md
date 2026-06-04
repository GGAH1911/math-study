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

# 무한급수의 수렴

## 정확한 진술

무한급수 $\sum_{n=1}^{\infty} a_n = a_1 + a_2 + a_3 + \cdots$는 다음과 같이 정의합니다. 먼저 **부분합** $S_N$을 처음 $N$개 항의 합으로 정의합니다:

$$S_N = \sum_{n=1}^{N} a_n = a_1 + a_2 + \cdots + a_N$$

무한급수가 **수렴한다**는 것은 부분합의 수열 $\{S_N\}$이 어떤 유한한 값 $S$로 수렴한다는 뜻입니다:

$$\lim_{N \to \infty} S_N = S$$

이때 $S$를 그 무한급수의 **합**이라 하며, $\sum_{n=1}^{\infty} a_n = S$로 나타냅니다. 만약 부분합의 극한이 존재하지 않거나 무한대로 발산하면 급수는 **발산한다**고 합니다.

## 직관과 기하적 의미

무한히 많은 수를 더하는 것은 얼핏 불가능해 보이지만, 부분합의 수열이 어떤 값에 점점 가까워지면 그 값을 합으로 정의하는 것입니다. 이는 수열의 극한 개념을 확장한 것으로, 더 이상 더할 것이 없을 때의 "최종 값"을 수학적으로 잡아냅니다. 예를 들어 등비급수에서는 공비의 절댓값이 1보다 작으면 항들이 계속 작아져서 합이 유한한 값에 수렴합니다.

## 한 줄 예

공비가 $\frac{1}{2}$인 등비급수 $\sum_{n=1}^{\infty} 1 \cdot \left(\frac{1}{2}\right)^{n-1} = 1 + \frac{1}{2} + \frac{1}{4} + \cdots$는 부분합 $S_N = \frac{1 - (1/2)^N}{1 - 1/2} \to 2$이므로 수렴값은 $2$입니다.
