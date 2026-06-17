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

# 삼각함수 기본값

## 정확한 진술

삼각함수의 **기본값**은 $0°, 30°, 45°, 60°, 90°$ (라디안으로는 $0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$) 같은 특수각에서 사인, 코사인, 탄젠트 함수가 가지는 값들을 의미합니다. 이들은 정확한 유리수나 무리수 형태로 표현되며, 다음과 같이 정리됩니다:

$$\begin{array}{c|cccccc}
\theta & 0° & 30° & 45° & 60° & 90° \\
\hline
\sin\theta & 0 & \frac{1}{2} & \frac{\sqrt{2}}{2} & \frac{\sqrt{3}}{2} & 1 \\
\cos\theta & 1 & \frac{\sqrt{3}}{2} & \frac{\sqrt{2}}{2} & \frac{1}{2} & 0 \\
\tan\theta & 0 & \frac{1}{\sqrt{3}} & 1 & \sqrt{3} & \text{정의되지 않음}
\end{array}$$

## 직관과 기하적 의미

단위원 위에서 각 $\theta$에 대응하는 점의 좌표가 $(\cos\theta, \sin\theta)$입니다. 기본값들은 **정삼각형**과 **정사각형**의 기하학적 성질에서 자연스럽게 나타납니다. 예를 들어, $45°$는 정사각형의 대각선에서 $\sin 45° = \cos 45° = \frac{\sqrt{2}}{2}$를 얻고, $30°$와 $60°$는 정삼각형을 반으로 자른 직각삼각형에서 유래합니다. 이 값들을 암기하는 것은 더 복잡한 각도의 삼각함수를 덧셈 공식이나 합성 공식으로 구할 때 필수입니다.

## 한 줄 예

$\sin 60° = \frac{\sqrt{3}}{2}$는 한 변의 길이가 2인 정삼각형을 높이로 반으로 나눈 직각삼각형에서 높이가 $\sqrt{3}$이므로, $\sin 60° = \frac{\sqrt{3}}{2}$입니다.

```python
# 검증: sympy.sin(sympy.pi/3), sympy.cos(sympy.pi/6)  → sqrt(3)/2
```
