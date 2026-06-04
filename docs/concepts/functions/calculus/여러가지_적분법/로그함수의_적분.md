---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지_적분법.md]
enables: []
mastery: unknown
---

# 로그함수의 적분

## 정확한 진술

자연로그함수 $\ln x$를 적분하면 다음을 얻습니다:
$$\int \ln x \, dx = x \ln x - x + C$$

일반적으로, 밑이 $a > 0$, $a \neq 1$인 로그함수의 적분은:
$$\int \log_a x \, dx = \frac{x \ln x - x}{\ln a} + C = \frac{x}{\ln a}(\log_a x - 1) + C$$

여기서 $C$는 적분상수입니다.

## 직관과 유도 과정

이 공식은 **부분적분**을 사용하여 유도됩니다. $\int \ln x \, dx$를 계산할 때:
- $u = \ln x$, $dv = dx$로 놓으면
- $du = \frac{1}{x} dx$, $v = x$

부분적분 공식 $\int u \, dv = uv - \int v \, du$를 적용하면:
$$\int \ln x \, dx = x \ln x - \int x \cdot \frac{1}{x} \, dx = x \ln x - \int 1 \, dx = x \ln x - x + C$$

기하학적으로 보면, 곡선 $y = \ln x$ 아래의 넓이가 직사각형과 삼각형 영역들의 조합으로 표현되는 원리입니다.

## 예제

$\int_1^e \ln x \, dx$를 계산하면:
$$\left[ x \ln x - x \right]_1^e = (e \ln e - e) - (1 \cdot 0 - 1) = e - e + 1 = 1$$

`sympy.integrate(sympy.log(x), (x, 1, sympy.E))` 실행 결과: $1$
