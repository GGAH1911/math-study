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

# 지수항의 극한

## 정확한 진술

지수항 $\{a^n\}$의 극한은 밑 $a$의 값에 따라 결정됩니다:

$$\lim_{n \to \infty} a^n = \begin{cases}
\infty & \text{if } a > 1 \\
1 & \text{if } a = 1 \\
0 & \text{if } |a| < 1 \\
\text{발산} & \text{if } a \leq -1
\end{cases}$$

여기서 수열 $\{a^n\}$은 $n$번째 항이 $a^n$인 수열을 나타냅니다.

## 직관 및 기하적 의미

지수항의 극한은 **밑의 크기**로 직관적으로 이해할 수 있습니다.

- **$a > 1$일 때**: 매번 $a$배씩 커지므로 계속 무한히 증가합니다. 예를 들어 $2^n$은 2, 4, 8, 16, ...으로 빠르게 커집니다.

- **$0 < a < 1$일 때**: 매번 $a$배씩 작아지므로 0에 가까워집니다. 예를 들어 $(\frac{1}{2})^n$은 $\frac{1}{2}, \frac{1}{4}, \frac{1}{8}, ...$로 빠르게 0으로 수렴합니다.

- **$|a| \geq 1$이고 $a \neq 1$일 때**: 항의 부호가 계속 바뀌거나 절댓값이 커지므로 수렴하지 않습니다.

이것은 **지수함수** $y = a^x$의 거동을 정수 입력에서 본 것입니다.

## 한 줄 예시

$\lim_{n \to \infty} 3^n = \infty$ (3배씩 계속 증가)

$\lim_{n \to \infty} (\frac{1}{3})^n = 0$ (3분의 1씩 계속 감소)

$\lim_{n \to \infty} (-2)^n$ = 발산 (부호가 진동하며 절댓값은 증가)

`sympy.limit(3**n, n, oo)` → $\infty$, `sympy.limit((Rational(1,3))**n, n, oo)` → $0$
