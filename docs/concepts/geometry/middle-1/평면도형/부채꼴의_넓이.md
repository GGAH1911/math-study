---
unit: 평면도형
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중1
prerequisites: [docs/concepts/geometry/middle-3/원의_성질.md]
enables: []
mastery: unknown
---

# 부채꼴의 넓이

## 정확한 진술

반지름 $r$인 원에서 중심각이 $\theta$ (라디안) 또는 $\alpha°$ (도)인 부채꼴의 넓이는 다음과 같습니다.

**라디안 표현:**
$$S = \frac{1}{2}r^2\theta$$

**도(degree) 표현:**
$$S = \frac{\pi r^2 \alpha}{360}$$

여기서 $r$은 원의 반지름, $\theta$는 중심각(라디안), $\alpha$는 중심각(도)입니다.

## 직관/기하적 의미

부채꼴은 원의 중심에서 원 위의 두 점을 이은 호에 의해 만들어지는 도형입니다. 부채꼴의 넓이는 **원 전체의 넓이에 중심각이 차지하는 비율을 곱한 것**입니다.

원 전체의 넓이는 $\pi r^2$이고, 한 바퀴 각도가 라디안으로 $2\pi$일 때 부채꼴이 차지하는 비율은 $\frac{\theta}{2\pi}$이므로:

$$S = \pi r^2 \cdot \frac{\theta}{2\pi} = \frac{1}{2}r^2\theta$$

중심각이 클수록, 그리고 원의 반지름이 클수록 부채꼴의 넓이가 증가합니다.

## 한 줄 예

반지름이 $3$이고 중심각이 $\frac{\pi}{3}$ (라디안)인 부채꼴의 넓이는 $S = \frac{1}{2} \times 3^2 \times \frac{\pi}{3} = \frac{3\pi}{2}$입니다 (sympy: `from sympy import pi; (1/2) * 9 * (pi/3)`).
