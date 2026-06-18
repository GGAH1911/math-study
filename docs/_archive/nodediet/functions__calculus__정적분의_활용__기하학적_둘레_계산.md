---
unit: 정적분의 활용
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/geometry/geometry-elective/이차곡선.md]
enables: []
mastery: unknown
---

# 기하학적 둘레 계산

## 정확한 진술

곡선의 **기하학적 둘레**(또는 호의 길이)는 그 곡선을 따라 측정한 거리입니다. 곡선이 $y=f(x)$ 형태로 주어질 때, 구간 $[a, b]$에서의 호의 길이는 다음 적분으로 정의됩니다:

$$L = \int_a^b \sqrt{1 + \left(\frac{dy}{dx}\right)^2} \, dx$$

또는 매개변수 표현 $\mathbf{r}(t) = (x(t), y(t))$로 주어질 때:

$$L = \int_{t_1}^{t_2} \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$$

## 직관/기하적 의미

곡선을 작은 직선 조각들로 나누면, 각 조각의 길이는 피타고라스 정리로 계산됩니다. $\Delta x$와 $\Delta y$ 변화에 대해 $\sqrt{(\Delta x)^2 + (\Delta y)^2}$이 조각의 길이이고, 이를 모두 더한 후 극한을 취하면 위 적분식이 됩니다. 따라서 이 정의는 곡선을 점점 더 짧은 일직선 세그먼트로 근사하는 과정에서 나타나는 자연스러운 개념입니다.

## 한 줄 예

반지름 $r$인 원은 매개변수 $(r\cos\theta, r\sin\theta)$로 표현되며, $\theta \in [0, 2\pi]$에서의 호의 길이는 $L = \int_0^{2\pi} r \, d\theta = 2\pi r$입니다.

**참고**: 이차곡선 중 **원**의 둘레는 위 공식으로 $2\pi r$를 얻지만, **타원**, **포물선**, **쌍곡선** 호의 길이는 초등함수로 표현되지 않으며 수치적분이나 특수함수를 사용하여 계산합니다.
