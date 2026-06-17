---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/함수의_극한과_연속.md]
enables: []
mastery: unknown
---

# 기본 극한

## 함수의 극한의 정의

$x$가 $a$에 가까워질 때, 함수값 $f(x)$가 어떤 값 $L$에 한없이 가까워지면 "$x \to a$일 때 $f(x)$의 극한은 $L$이다"라고 하고, 기호로 $\lim_{x \to a} f(x) = L$로 나타냅니다.

**엄밀한 정의(ε-δ 정의)**: 임의의 양수 $\varepsilon$에 대하여, 다음을 만족하는 양수 $\delta$가 존재할 때, $\lim_{x \to a} f(x) = L$입니다.

$$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon$$

이는 "$x$를 $a$에 충분히 가깝게 잡으면 $f(x)$를 $L$에 임의로 가깝게 만들 수 있다"는 의미입니다.

## 기하적 의미

$y = f(x)$ 그래프를 생각해봅시다. $\lim_{x \to a} f(x) = L$은 다음을 의미합니다:

- $x$축에서 $a$ 근처 구간 $(a-\delta, a+\delta)$의 모든 점 $x$ (단, $x \ne a$)에 대해
- 대응하는 함수값 $f(x)$가 $L$ 근처 띠 $(L-\varepsilon, L+\varepsilon)$ 안에 들어간다

여기서 **$x=a$에서의 함숫값 $f(a)$는 극한값과 무관**합니다. $x$가 $a$에 다가갈 때의 *경향*을 나타낼 뿐입니다.

## 예시

$\lim_{x \to 2} (3x - 1) = 5$

$x$가 2에 가까워질수록 $3x-1$은 5에 가까워집니다. 예: $x=2.01$일 때 $f(x)=5.03$, $x=1.99$일 때 $f(x)=4.97$. 

`sympy: from sympy import limit, symbols, Function; x = symbols('x'); limit(3*x - 1, x, 2)` → $5$ ✓

## 주의

극한값 $L$이 존재하려면 **좌극한과 우극한이 같아야 합니다**. 즉, $\lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x)$일 때만 극한이 존재합니다.
