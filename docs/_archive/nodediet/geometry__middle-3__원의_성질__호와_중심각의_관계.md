---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-3/원의_성질.md]
enables: []
mastery: unknown
---

# 호와 중심각의 관계

## 정확한 진술

원의 중심을 $O$, 반지름을 $r$이라 하자. 원 위의 두 점 $A$, $B$에 대해:
- **호 $\mathbf{AB}$**: 원 위의 점 $A$에서 점 $B$까지의 원 위의 경로
- **중심각**: 호 $AB$에 대응하는 중심 $O$에서의 각 $\angle AOB$ (도 단위)

호의 길이는 중심각에 정확히 비례한다. 중심각이 $\theta°$일 때, 호의 길이 $l$은:
$$l = \frac{\theta}{360} \times 2\pi r = \frac{\theta \pi r}{180}$$

또는 중심각이 $\theta$ 라디안이면:
$$l = r\theta$$

## 직관/기하적 의미

원 전체를 한 바퀴 도는 호(360°)의 길이는 원의 둘레 $2\pi r$입니다. 중심각이 360°의 일부이면, 호의 길이도 원 둘레의 같은 비율입니다. 

예를 들어 중심각이 180°(반원)이면 호의 길이는 $\pi r$(원 둘레의 절반)이고, 중심각이 90°(사분원)이면 호의 길이는 $\frac{\pi r}{2}$(원 둘레의 1/4)입니다. **호의 길이와 중심각은 정비례 관계**이므로, 중심각이 클수록 호의 길이도 커집니다.

## 한 줄 예

반지름 $6\text{cm}$인 원에서 중심각이 $60°$인 호의 길이는 $\frac{60}{360} \times 2\pi \times 6 = 2\pi\text{ cm}$입니다. (`sympy.pi * 6 * 60 / 180` = $2\pi$)
