---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/미분.md]
enables: []
mastery: unknown
---

# 미분 계산

## 미분의 정의

함수 $f(x)$의 $x = a$에서의 **미분계수**는 다음 극한값입니다.

$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

이 극한이 존재할 때, $f(x)$는 $x = a$에서 **미분가능**하다고 합니다. 모든 $x$에서 미분계수를 구한 함수를 $f(x)$의 **도함수**라 하고 $f'(x)$로 나타냅니다.

## 기하적 의미

미분계수 $f'(a)$는 **곡선 $y = f(x)$ 위의 점 $(a, f(a))$에서의 접선의 기울기**입니다. 

$h$가 0에 가까워질수록, 두 점 $(a, f(a))$와 $(a+h, f(a+h))$를 지나는 할선(secant line)의 기울기 $\frac{f(a+h) - f(a)}{h}$는 접선의 기울기로 수렴합니다. 따라서 미분계수는 그 점에서의 **순간 변화율**을 나타냅니다.

## 기본 계산 규칙

미분계수의 정의로부터 다음 규칙들을 유도할 수 있습니다.

- 상수: $(c)' = 0$
- 멱함수: $(x^n)' = nx^{n-1}$ (단, $n$은 자연수)
- 합과 차: $(f \pm g)' = f' \pm g'$
- 곱: $(fg)' = f'g + fg'$
- 몫: $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$ (단, $g \neq 0$)

## 한 줄 예

$f(x) = x^3$일 때, 미분의 정의를 사용하면 $f'(x) = 3x^2$이고, $x=2$에서의 접선의 기울기는 $f'(2) = 12$입니다.

```python
# sympy로 검산: 
# from sympy import *; x = symbols('x'); f = x**3; diff(f, x).subs(x, 2)
# 결과: 12
```
