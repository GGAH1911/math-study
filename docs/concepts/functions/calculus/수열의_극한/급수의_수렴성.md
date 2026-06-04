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

# 급수의 수렴성

## 정확한 진술

급수 $\sum_{n=1}^{\infty} a_n$이 **수렴한다**는 것은 부분합의 수열이 극한값을 가진다는 뜻입니다. 여기서 $N$번째 부분합을 $S_N = a_1 + a_2 + \cdots + a_N$이라 할 때, 다음이 성립합니다:

$$\lim_{N \to \infty} S_N = S \quad (\text{유한한 실수})$$

이 극한값 $S$를 급수의 합이라 부릅니다. 극한값이 존재하지 않거나 $\pm \infty$이면 급수는 **발산**합니다.

## 직관과 기하적 의미

무한히 많은 항을 더하는데 그 합이 유한한 값에 도달한다는 것이 핵심 아이디어입니다. 이는 수열의 극한 개념을 "합"으로 확장한 것입니다.

구체적으로, 항 $a_n$이 0으로 빠르게 수렴하면 뒤로 갈수록 더해지는 값의 기여도가 무시할 수 있을 정도로 작아집니다. 예를 들어 기하급수는 공비 $|r| < 1$일 때 수렴하는데, 이는 각 항이 기하급수적으로 감소하기 때문입니다:

$$\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots \to 1$$

이처럼 "무한 과정"이 실제로 유한한 값으로 닫혀간다는 의미에서 수렴은 해석학의 중요한 개념입니다.

## 한 줄 예

기하급수 $\sum_{n=1}^{\infty} \left(\frac{1}{3}\right)^n$은 $S = \frac{1/3}{1-1/3} = \frac{1}{2}$로 수렴합니다.

(`sympy.summation(Rational(1,3)**n, (n, 1, oo))` 검증 가능)
