---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 수와식
prerequisites: [docs/concepts/geometry/middle-2/닮음과_피타고라스.md, docs/concepts/equations/high-1/방정식과_부등식.md]
enables: []
mastery: unknown
---

# AM-GM 부등식

## 정의

양의 실수 $a, b$에 대해 산술평균(AM)은 기하평균(GM) 이상임을 나타내는 부등식이다:

$$\frac{a + b}{2} \geq \sqrt{ab}$$

등호는 $a = b$일 때 성립한다. $n$개의 양의 실수 $a_1, a_2, \ldots, a_n$으로 일반화하면 $\dfrac{a_1 + a_2 + \cdots + a_n}{n} \geq \sqrt[n]{a_1 a_2 \cdots a_n}$이며, 등호는 모든 $a_i$가 같을 때 성립한다. 합이 일정할 때 곱의 최댓값, 또는 곱이 일정할 때 합의 최솟값을 구할 때 활용한다.

## 예시

양수 $x$에 대해 $x + \dfrac{4}{x}$의 최솟값을 구하시오.

AM-GM 부등식 적용:

$$x + \frac{4}{x} \geq 2\sqrt{x \cdot \frac{4}{x}} = 2\sqrt{4} = 4$$

등호는 $x = \dfrac{4}{x}$, 즉 $x = 2$일 때 성립. 따라서 최솟값은 $4$.

## 관련 개념

- 부등식의 성질
- 코시-슈바르츠 부등식
- 이차부등식
- 최대·최솟값
