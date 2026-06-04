---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 고1
prerequisites: [docs/concepts/functions/high-1/함수와_그래프.md]
enables: []
mastery: unknown
---

# 좌표와 도형의 넓이

## 정확한 진술

좌표 평면에서 주어진 도형(다각형, 곡선으로 둘러싸인 영역 등)이 차지하는 면적을 좌표의 값들을 이용해 수치로 구하는 것을 **좌표와 도형의 넓이**라 합니다. 일반적으로 도형의 꼭짓점 좌표나 경계를 나타내는 함수를 알 때, 이들로부터 넓이를 계산합니다.

## 직관·기하적 의미

평면 위의 도형은 좌표를 이용해 정확히 위치시킬 수 있고, 각 부분이 좌표축과 맺는 관계를 통해 넓이를 구할 수 있습니다.

**다각형의 경우**: 꼭짓점들의 좌표가 주어지면, 삼각형은 밑변×높이÷2 공식이나 좌표로부터 직접 계산하고, 사각형도 변의 길이와 각도로부터 구합니다.

**곡선으로 둘러싸인 영역의 경우**: 함수 $y = f(x)$와 $x$축 사이의 넓이는 정적분 $\displaystyle \int_a^b |f(x)| \, dx$로 구합니다.

**신발끈 공식(Shoelace formula)**: 꼭짓점이 $(x_1, y_1), (x_2, y_2), \ldots, (x_n, y_n)$인 다각형의 넓이는
$$A = \frac{1}{2} \left| \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i) \right|$$
(단, $(x_{n+1}, y_{n+1}) = (x_1, y_1)$)

## 한 줄 예

꼭짓점이 $(0, 0)$, $(4, 0)$, $(2, 3)$인 삼각형의 넓이는 신발끈 공식으로 $\frac{1}{2}|0 \cdot 0 - 4 \cdot 0 + 4 \cdot 3 - 2 \cdot 0 + 2 \cdot 0 - 0 \cdot 3| = 6$입니다.

```python
# sympy로 검산: 삼각형 넓이 = 6
from sympy import Rational
A = Rational(1, 2) * abs(0*0 - 4*0 + 4*3 - 2*0 + 2*0 - 0*3); print(A)
```
