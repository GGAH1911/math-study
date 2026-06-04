---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 중3
prerequisites: [docs/concepts/functions/middle-3/이차함수.md]
enables: []
mastery: unknown
---

# 직선과 이차함수의 교점

## 정확한 진술

직선과 이차함수의 교점이란 직선의 방정식과 이차함수의 방정식을 동시에 만족하는 점(들)을 말합니다. 직선 $y = ax + b$와 이차함수 $y = px^2 + qx + r$ (단, $p \neq 0$)이 주어졌을 때, 두 식을 같다고 놓으면

$$px^2 + qx + r = ax + b$$

이를 정리하면

$$px^2 + (q - a)x + (r - b) = 0$$

이 이차방정식의 해가 교점의 $x$좌표이고, 이를 원래 식에 대입하면 $y$좌표를 구할 수 있습니다.

## 직관/기하적 의미

좌표평면 위에서 직선과 포물선이 만나는 자리입니다. 이차방정식의 판별식 $D = (q-a)^2 - 4p(r-b)$에 따라:
- $D > 0$: 서로 다른 두 점에서 만남 (할선)
- $D = 0$: 한 점에서 만남 (접선)  
- $D < 0$: 만나지 않음

직선과 포물선의 **위치 관계**를 판정하는 핵심 도구이며, 교점의 개수와 좌표는 함수의 그래프, 부등식의 영역, 최댓값·최솟값 문제 등에서 자주 필요합니다.

## 한 줄 예

직선 $y = x + 1$과 이차함수 $y = x^2$의 교점을 구하려면 $x^2 = x + 1$, 즉 $x^2 - x - 1 = 0$을 풀어 $x = \frac{1 \pm \sqrt{5}}{2}$를 얻고, 각각을 $y = x + 1$에 대입하여 두 교점 $\left(\frac{1 + \sqrt{5}}{2}, \frac{3 + \sqrt{5}}{2}\right)$, $\left(\frac{1 - \sqrt{5}}{2}, \frac{3 - \sqrt{5}}{2}\right)$을 구합니다. (`sympy.solve(x**2 - x - 1, x)` → $\left[\frac{1 - \sqrt{5}}{2}, \frac{1 + \sqrt{5}}{2}\right]$)
