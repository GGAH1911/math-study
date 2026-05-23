---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 중1
prerequisites: [docs/concepts/functions/middle-1/좌표평면과_그래프.md]
enables: []
mastery: unknown
---

# 원점대칭

함수의 그래프가 원점을 중심으로 점대칭을 이루는 성질입니다. 좌표평면 단원에서 함수의 대칭성을 판별할 때 사용됩니다.

## 정의

좌표평면에서 한 도형이 원점에 대한 점대칭이라는 것은, 도형 위의 임의의 점 $(x, y)$에 대해 점 $(-x, -y)$도 그 도형 위에 있다는 것입니다.

함수 $y = f(x)$의 그래프가 원점대칭이 되는 것은 모든 $x$에 대해
$$f(-x) = -f(x)$$
가 성립할 때이며, 이때 $f$를 **기함수**라 합니다.

## 예시

$f(x) = x^3$은 모든 $x$에 대해 $f(-x) = -x^3 = -f(x)$이므로 원점대칭입니다(기함수).

또한 $f(x) = \dfrac{1}{x}$ ($x \neq 0$)도 $f(-x) = -\dfrac{1}{x} = -f(x)$이므로 그래프가 원점대칭입니다.

반면 $f(x) = x^2$은 $f(-x) = x^2 = f(x)$로 $y$축 대칭(우함수)이며 원점대칭이 아닙니다.

## 관련 개념

- [원점 대칭이동](docs/concepts/functions/middle-1/좌표평면과_그래프/원점_대칭이동.md)
- [축 대칭](docs/concepts/functions/middle-1/좌표평면과_그래프/축_대칭.md)
- [좌표평면과 그래프](docs/concepts/functions/middle-1/좌표평면과_그래프.md)
