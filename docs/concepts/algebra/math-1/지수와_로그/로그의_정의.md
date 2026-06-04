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

# 로그의 정의

## 정확한 진술

$a > 0, a \neq 1$일 때, 양수 $x$에 대해 $a^y = x$를 만족하는 실수 $y$를 **$a$를 밑으로 하는 $x$의 로그**(logarithm)라 하고, $\log_a x$로 나타냅니다.

즉, $a^y = x \Leftrightarrow y = \log_a x$입니다.

이때 $a$를 **밑**(base), $x$를 **진수**(argument)라 부릅니다. 진수는 반드시 양수여야 합니다.

## 직관: 지수의 역함수

로그는 **"지수 함수의 역함수"**입니다. 지수 함수 $y = a^x$에서 $x$와 $y$의 역할을 바꾼 것이 로그 함수입니다.

예를 들어 "2를 몇 번 곱해야 8이 될까?"라는 질문에 답하는 것이 로그입니다. $2^3 = 8$이므로 $\log_2 8 = 3$입니다. 

다시 말해, **로그는 "어떤 수를 밑으로 하여 주어진 수에 도달하려면 몇 번 곱해야 하는가"를 구하는 연산**입니다.

## 한 줄 예

$3^4 = 81$이므로 $\log_3 81 = 4$입니다.

더 계산하면: $10^2 = 100$이므로 $\log_{10} 100 = 2$이고, $\left(\frac{1}{2}\right)^{-2} = 4$이므로 $\log_{1/2} 4 = -2$입니다.

**검산**: `sympy.log(81, 3)` → 4, `sympy.log(100, 10)` → 2

## 특수한 경우

- **상용로그**(common logarithm): 밑이 10인 로그. $\log_{10} x$를 보통 $\log x$로 쓰기도 합니다.
- **자연로그**(natural logarithm): 밑이 $e$(자연상수)인 로그. $\log_e x = \ln x$로 나타냅니다.

이 두 로그는 수능과 대학 수학에서 가장 자주 등장합니다.
