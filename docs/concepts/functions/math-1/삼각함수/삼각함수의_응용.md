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

# 삼각함수의 응용

## 정확한 진술

삼각함수의 응용이란 각도, 파동, 주기 현상을 다루는 실제 문제를 삼각함수의 성질(주기성, 대칭성, 덧셈 공식)로 모델링하고 해결하는 것입니다. 예각삼각형의 정현법칙이나 코사인법칙으로 미지의 변의 길이를 구하거나, $y = A\sin(Bx + C) + D$ 형태의 함수로 진동 운동을 표현하고 최댓값/최솟값을 찾는 것이 핵심입니다.

## 직관/기하적 의미

삼각함수는 각도와 길이의 관계를 나타내므로, 건물의 높이를 재거나 멀리 떨어진 물체까지의 거리를 구할 때 직접 측정할 수 없는 상황에서 활약합니다. 관측자의 눈 높이와 각도를 알면 정현법칙 $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$로 모든 변을 복원할 수 있습니다. 또한 물결이나 음파 같은 주기 운동은 $y = A\sin(\omega t + \phi)$로 쓸 수 있고, 최댓값은 $|A|$, 주기는 $\frac{2\pi}{\omega}$이므로 물리 현상을 예측할 수 있습니다. 회전, 진동, 파동—이들은 모두 각도 변화로 설명되며, 그것이 삼각함수의 언어입니다.

## 한 줄 예

삼각형의 두 변의 길이가 $5$, $7$이고 그 사이의 각이 $60°$일 때, 코사인법칙 $c^2 = 5^2 + 7^2 - 2 \cdot 5 \cdot 7 \cdot \cos 60°$로 세 번째 변 $c = \sqrt{39}$를 구합니다. (`from sympy import sqrt, cos, pi; c = sqrt(25 + 49 - 70*cos(pi/3)); print(c)`)
