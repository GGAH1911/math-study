---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 수학1
prerequisites: [docs/concepts/algebra/math-1/지수와_로그.md]
enables: []
mastery: unknown
---

# 로그의 덧셈과 뺄셈

## 정확한 진술

로그의 덧셈과 뺄셈은 다음과 같이 정의됩니다.

$$\log_a(x) + \log_a(y) = \log_a(xy)$$

$$\log_a(x) - \log_a(y) = \log_a\left(\frac{x}{y}\right)$$

여기서 밑 $a$는 $a > 0$이고 $a \neq 1$이며, $x, y > 0$입니다.

## 직관 및 유도

이 성질은 지수법칙에서 자연스럽게 따라옵니다. $\log_a(x) = m$, $\log_a(y) = n$이라고 하면, 로그의 정의에 의해 $a^m = x$, $a^n = y$입니다.

두 수를 곱하면:
$$xy = a^m \cdot a^n = a^{m+n}$$

양변에 로그를 취하면:
$$\log_a(xy) = m + n = \log_a(x) + \log_a(y)$$

비슷하게 나눗셈의 경우:
$$\frac{x}{y} = \frac{a^m}{a^n} = a^{m-n}$$

따라서:
$$\log_a\left(\frac{x}{y}\right) = m - n = \log_a(x) - \log_a(y)$$

본질적으로 **로그는 곱셈을 덧셈으로, 나눗셈을 뺄셈으로 변환**하는 도구입니다. 이것이 로그가 역사적으로 복잡한 계산을 간단히 하기 위해 발명된 이유입니다.

## 예

$\log_2(8) + \log_2(4)$를 계산하면:
$$\log_2(8) + \log_2(4) = \log_2(8 \times 4) = \log_2(32) = 5$$

또는 $\log_2(16) - \log_2(4)$는:
$$\log_2(16) - \log_2(4) = \log_2\left(\frac{16}{4}\right) = \log_2(4) = 2$$
