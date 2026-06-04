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

# 극한값의 성질

## 정확한 진술

수열 $\{a_n\}$과 $\{b_n\}$이 각각 $a$, $b$로 수렴할 때, 다음이 성립합니다:

$$\lim_{n \to \infty} (a_n + b_n) = a + b$$

$$\lim_{n \to \infty} (a_n - b_n) = a - b$$

$$\lim_{n \to \infty} (a_n \cdot b_n) = a \cdot b$$

$$\lim_{n \to \infty} \frac{a_n}{b_n} = \frac{a}{b} \quad (b \neq 0)$$

또한 상수 $c$에 대해 $\lim_{n \to \infty} c \cdot a_n = c \cdot a$가 성립하고, $a_n \leq b_n$이면 $a \leq b$입니다(비교 정리).

## 직관/기하적 의미

극한값의 성질은 "극한을 구하는 계산을 조각으로 나누어 할 수 있다"는 의미입니다. 두 수열이 각각 어떤 값으로 안정화(수렴)한다면, 이들을 더하거나 빼거나 곱하거나 나눈 수열도 예상되는 값으로 안정화합니다. 직관적으로는 당연하지만, 이를 엄밀하게 증명하려면 극한의 $\epsilon$-$N$ 정의와 부등식 조작이 필요합니다. 이 성질들이 있어야만 복잡한 분수식의 극한을 단순히 분자와 분모의 극한으로 각각 나누어 계산할 수 있습니다.

## 한 줄 예

$a_n = \frac{n+1}{n}$, $b_n = \frac{2n}{n}$일 때, $\lim_{n \to \infty} a_n = 1$, $\lim_{n \to \infty} b_n = 2$이므로 곱의 성질에 의해 $\lim_{n \to \infty} (a_n \cdot b_n) = 1 \times 2 = 2$입니다. (`sympy.limit((n+1)/n * 2*n/n, n, oo)` → 2)
