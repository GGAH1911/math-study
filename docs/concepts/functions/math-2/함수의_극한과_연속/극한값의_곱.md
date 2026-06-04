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

# 극한값의 곱

## 정확한 진술

두 함수 $f(x)$와 $g(x)$가 $x \to a$일 때 각각 극한값 $L$과 $M$을 가질 때, 그 곱 $f(x) \cdot g(x)$의 극한값은 극한값들의 곱입니다.

$$\lim_{x \to a} f(x) = L, \quad \lim_{x \to a} g(x) = M \implies \lim_{x \to a} f(x) \cdot g(x) = L \cdot M$$

이를 **극한값의 곱 법칙**이라 하며, 극한의 기본 성질 중 하나입니다.

## 직관과 의미

극한의 더하기 법칙처럼, 곱 법칙도 직관적입니다. $x$가 $a$에 가까워질 때 $f(x)$가 $L$로 수렴하고 $g(x)$가 $M$으로 수렴하면, 두 값을 곱한 결과도 $L \times M$으로 자연스럽게 수렴합니다. 

예를 들어 길이가 $L$으로 수렴하는 선분과 폭이 $M$으로 수렴하는 선분이 있다면, 그 직사각형의 넓이는 $L \times M$으로 수렴하는 것과 같습니다. 이는 극한값이 가지는 **안정성**을 보여줍니다.

특히 $f(x) = g(x)$인 경우, 
$$\lim_{x \to a} [f(x)]^2 = \left[\lim_{x \to a} f(x)\right]^2$$
가 성립하며, 이를 이용해 제곱이나 거듭제곱 형태의 극한을 계산할 수 있습니다.

## 한 줄 예

$\lim_{x \to 2} (x+1) = 3$이고 $\lim_{x \to 2} x = 2$이므로, $\lim_{x \to 2} (x+1) \cdot x = 3 \times 2 = 6$입니다. (검증: `sympy.limit((x+1)*x, x, 2)`)

## 주의

곱 법칙이 성립하려면 **두 극한값이 모두 존재해야** 합니다. 한쪽이 존재하지 않으면 곱의 극한값도 보장되지 않으며, $\infty \times 0$ 같은 부정형에서는 별도의 분석이 필요합니다.
