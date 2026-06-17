---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md]
enables: []
mastery: unknown
---

# 부채꼴의 기하학

## 정확한 진술

중심이 원점, 반지름이 $r > 0$인 원에서 중심각 $\theta$ (단위: 라디안, $0 < \theta \leq 2\pi$)로 결정되는 부채꼴은 두 개의 반지름과 그 사이의 호로 경계지어진 영역입니다. 부채꼴의 주요 성질은:
- **호의 길이**: $l = r\theta$
- **넓이**: $A = \frac{1}{2}r^2\theta$ 또는 $A = \frac{1}{2}rl$

## 직관과 기하적 의미

부채꼴은 원판을 중심에서 두 반지름 사이로 자른 "파이 조각" 모양입니다. 원 전체의 넓이가 $\pi r^2$이므로, 부채꼴이 차지하는 비율은 $\frac{\theta}{2\pi}$입니다. 극한의 관점에서 특별히 중요한 점은, 중심각이 0에 가까워질 때 부채꼴이 얇은 삼각형처럼 행동한다는 것입니다. 이 극한 과정에서 
$$\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$$
이라는 삼각함수의 기본 극한이 핵심 역할을 하며, 이것이 미분학에서 $\frac{d}{dx}\sin x = \cos x$를 유도하는 데 필수입니다. 따라서 부채꼴은 단순한 기하 도형이 아니라 극한과 미분을 잇는 교량입니다.

## 한 줄 예

반지름 3인 원에서 중심각이 $\frac{\pi}{4}$ (45°)인 부채꼴의 넓이는 $A = \frac{1}{2} \cdot 3^2 \cdot \frac{\pi}{4} = \frac{9\pi}{8}$입니다.
