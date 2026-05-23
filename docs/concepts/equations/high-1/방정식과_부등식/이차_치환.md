---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 방정식
grade: 고1
prerequisites: [docs/concepts/equations/high-1/방정식과_부등식.md]
enables: []
mastery: unknown
---

# 이차 치환

고차 방정식이나 부등식에서 반복되는 식을 새 변수로 놓아 이차식으로 환원하는 기법입니다. 고1 방정식과 부등식 단원의 표준 풀이 전략입니다.

## 정의

방정식 또는 부등식의 좌·우변이 어떤 식 $u = u(x)$의 이차식 꼴 $au^2 + bu + c$로 표현될 때, $u$를 새 변수로 치환하여 $u$에 관한 이차방정식·이차부등식으로 만듭니다. $u$의 해를 구한 다음, $u = u(x)$로 되돌려 $x$의 해를 얻습니다. 치환 후에는 $u$의 범위(예: $u \ge 0$ 등)에 주의합니다.

## 예시

방정식 $x^4 - 5x^2 + 4 = 0$을 풀어 봅니다. $u = x^2$로 두면 $u \ge 0$이고
$$u^2 - 5u + 4 = 0 \implies (u-1)(u-4) = 0 \implies u = 1\ \text{또는}\ u = 4.$$
$x^2 = 1$에서 $x = \pm 1$, $x^2 = 4$에서 $x = \pm 2$이므로 해는 $x = \pm 1, \pm 2$입니다.

또한 $(x^2 + x)^2 - 8(x^2 + x) + 12 = 0$에서 $u = x^2 + x$로 두면 $u^2 - 8u + 12 = 0$, $u = 2$ 또는 $u = 6$을 얻고 다시 $x^2 + x = 2$ 또는 $x^2 + x = 6$을 풉니다.

## 관련 개념

- [방정식과 부등식](docs/concepts/equations/high-1/방정식과_부등식.md)
- [이차부등식의 해법](docs/concepts/equations/high-1/방정식과_부등식/이차부등식의_해법.md)
