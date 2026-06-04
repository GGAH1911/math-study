---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 곡선 사이의 넓이

## 정확한 진술

구간 $[a, b]$에서 두 곡선 $y = f(x)$, $y = g(x)$가 있을 때, 이 두 곡선 사이의 넓이는 다음 정적분으로 정의됩니다.

$$S = \int_a^b |f(x) - g(x)| \, dx$$

일반적으로 $f(x) \geq g(x)$인 경우 절댓값 기호를 제거하여:

$$S = \int_a^b \{f(x) - g(x)\} \, dx$$

## 직관과 기하적 의미

곡선 사이의 넓이는 "위쪽 곡선에서 아래쪽 곡선을 뺀 높이"를 구간 전체에 걸쳐 누적한 것입니다. 좌표평면에서 두 곡선으로 둘러싸인 영역을 정적분으로 측정하는 방법입니다.

곡선이 교차하는 경우라면, 교점을 구한 후 각 부분 구간에서 위/아래를 판단하여 구간을 나누어 계산합니다. 예를 들어 $x = c$에서 교차한다면:

$$S = \int_a^c \{f(x) - g(x)\} \, dx + \int_c^b \{g(x) - f(x)\} \, dx$$

## 한 줄 예

$y = x^2$과 $y = 4$가 교차하는 구간 $[-2, 2]$에서 두 곡선 사이의 넓이는 $\int_{-2}^2 (4 - x^2) \, dx = \left[4x - \frac{x^3}{3}\right]_{-2}^2 = \frac{32}{3}$입니다.

```python
# 검증: sympy.integrate(4 - x**2, (x, -2, 2)) → 32/3
```
