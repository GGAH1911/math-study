---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# 삼각방정식의 풀이

## 삼각방정식의 정확한 진술

삼각방정식은 미지수 $x$에 대한 삼각함수 식을 포함하는 방정식입니다. 예컨대 $\sin x = \frac{1}{2}$, $\cos 2x + \sin x = 1$, $\tan x = \sqrt{3}$ 등이 모두 삼각방정식입니다. **삼각방정식을 푼다는 것**은 이 방정식을 만족하는 모든 $x$ 값을 찾는 것이며, 삼각함수의 **주기성** 때문에 보통 무한히 많은 해를 가집니다. 따라서 일반해(general solution)를 정수 매개변수 $k$를 포함한 형태로 나타냅니다.

## 기하적 의미와 풀이의 핵심

좌표평면에서 삼각함수 $y = \sin x$의 그래프와 수평선 $y = a$ (단, $-1 \leq a \leq 1$)의 교점의 $x$ 좌표들이 바로 $\sin x = a$의 모든 해입니다. 삼각함수가 주기 $2\pi$를 가지므로, 한 주기 내에서 찾은 기본해 $\alpha$에 대해 일반해는 $x = \alpha + 2\pi k$ 또는 $x = \pi - \alpha + 2\pi k$ 형태가 됩니다. 이는 삼각함수의 대칭성—$\sin(\pi - \theta) = \sin\theta$—에서 비롯됩니다. 코사인과 탄젠트도 마찬가지로, 특정 기본해를 구한 후 주기를 더하면 모든 해를 나타낼 수 있습니다.

## 풀이 전략과 한 줄 예

**풀이 절차**: (1) 삼각함수를 하나의 형태로 정리하거나 특수각(각도 $0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$ 등)과 연결되는 형태로 변형, (2) 그 각의 삼각함수 값을 알아서 기본해 찾기, (3) 주기를 더하여 일반해 표현.

**예**: $\sin x = \frac{1}{2}$의 경우, $\sin \frac{\pi}{6} = \frac{1}{2}$이므로 기본해는 $x = \frac{\pi}{6}$ 또는 $x = \pi - \frac{\pi}{6} = \frac{5\pi}{6}$입니다. 주기를 포함하면 **$x = \frac{\pi}{6} + 2\pi k$ 또는 $x = \frac{5\pi}{6} + 2\pi k$ (단, $k$는 정수)**가 일반해입니다.

(`sympy.solve(sp.sin(x) - sp.Rational(1,2), x)` 로 검증 가능)
