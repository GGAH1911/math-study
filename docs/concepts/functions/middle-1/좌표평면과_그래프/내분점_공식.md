---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 중1
prerequisites: [docs/concepts/functions/middle-1/좌표평면과_그래프.md]
enables: []
mastery: unknown
---

# 내분점 공식

## 정확한 진술

좌표평면 위의 두 점 $A(x_1, y_1)$과 $B(x_2, y_2)$를 잇는 선분 $AB$를 $m:n$으로 내분하는 점을 $P$라 할 때, 점 $P$의 좌표는 다음과 같습니다:

$$P = \left( \frac{nx_1 + mx_2}{m+n}, \frac{ny_1 + my_2}{m+n} \right)$$

여기서 $m > 0, n > 0$이며, 점 $P$는 $A$로부터 $B$ 방향으로 $\frac{m}{m+n}$만큼 떨어진 위치에 있습니다.

## 직관과 기하적 의미

내분점 공식은 두 점 사이의 거리를 일정한 비율로 배분하는 방법입니다. 예를 들어 선분 $AB$를 $2:1$로 내분한다는 것은, 점 $A$로부터 점 $B$로 향하면서 전체 거리의 $\frac{2}{3}$지점에 내분점이 위치한다는 뜻입니다.

공식의 핵심은 **가중 평균**입니다. 각 좌표는 반대편 비율을 가중치로 하여 계산됩니다. 즉, $A$의 좌표에는 $n$을, $B$의 좌표에는 $m$을 곱한 후 합을 $m+n$으로 나누는 것입니다. 이를 통해 점 $P$가 정확히 $m:n$의 비율로 선분을 나누는 위치가 됩니다.

## 기본 예제

$A(1, 2)$, $B(7, 8)$을 $1:2$로 내분하는 점의 좌표를 구하면:

$$x = \frac{2 \cdot 1 + 1 \cdot 7}{1+2} = \frac{9}{3} = 3$$
$$y = \frac{2 \cdot 2 + 1 \cdot 8}{1+2} = \frac{12}{3} = 4$$

따라서 내분점은 $P(3, 4)$입니다. (검증: `from sympy import Point; A = Point(1,2); B = Point(7,8); P = Point(3,4); print(P.distance(A), P.distance(B))`)

**특수한 경우**: $m=n$일 때 내분점은 선분의 중점이 되며, 좌표는 $\left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$입니다.
