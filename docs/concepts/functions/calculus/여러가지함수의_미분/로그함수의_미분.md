---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_미분.md]
enables: []
mastery: unknown
---

# 로그함수의 미분

## 정확한 진술

자연로그 함수 $\ln x$ ($x > 0$)의 도함수는 다음과 같습니다:

$$(\ln x)' = \frac{1}{x}$$

일반적으로 밑이 $a$ ($a > 0, a \neq 1$)인 로그함수 $\log_a x$의 도함수는:

$$(\log_a x)' = \frac{1}{x \ln a}$$

## 유도 과정

로그함수는 지수함수의 역함수이므로 **역함수의 미분법**을 사용합니다.

$y = \ln x$이면 $e^y = x$이므로, 양변을 $x$로 미분하면:
$$e^y \cdot \frac{dy}{dx} = 1$$

따라서:
$$\frac{dy}{dx} = \frac{1}{e^y} = \frac{1}{x}$$

일반 로그의 경우, **밑의 변환 공식** $\log_a x = \frac{\ln x}{\ln a}$를 이용하면:
$$(\log_a x)' = \frac{1}{\ln a} \cdot (\ln x)' = \frac{1}{x \ln a}$$

## 기하적 의미

도함수 $\frac{1}{x}$는 $x$가 증가함에 따라 감소합니다. 즉, 로그함수의 그래프는 점점 완만해집니다. $x=1$에서 기울기는 1이고, $x$가 크면 기울기는 0에 가까워집니다.

## 예시

$(\log_2 x)'$를 구하면:
$$(\log_2 x)' = \frac{1}{x \ln 2}$$

$x = 2$에서의 기울기는 $\frac{1}{2 \ln 2} \approx 0.721$입니다.

검산: `sympy.diff(sympy.log(x, 2), x)` → $\frac{1}{x \ln(2)}$ ✓
