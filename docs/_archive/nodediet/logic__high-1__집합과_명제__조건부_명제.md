---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 논리
grade: 고1
prerequisites: [docs/concepts/logic/high-1/집합과_명제.md]
enables: []
mastery: unknown
---

# 조건부 명제

## 정확한 진술

두 명제 $p$, $q$에 대하여 "$p$이면 $q$이다"의 형태로 표현되는 명제를 **조건부 명제**(conditional proposition)라 하고, 이를 $p \to q$ 또는 $p \Rightarrow q$로 나타냅니다. 여기서 $p$를 **가정**(전제, antecedent), $q$를 **결론**(consequent)이라 부릅니다.

조건부 명제 $p \to q$의 진릿값은 다음 진리표를 따릅니다.

| $p$ | $q$ | $p \to q$ |
|---|---|---|
| T | T | T |
| T | F | **F** |
| F | T | T |
| F | F | T |

즉, $p \to q$는 **$p$가 참이면서 $q$가 거짓인 경우에만 거짓**입니다.

## 직관적 의미

조건부 명제 $p \to q$는 "가정 $p$가 참이면, 반드시 결론 $q$도 참이어야 한다"는 약속입니다. 명제가 거짓이 되려면 이 약속이 깨져야 하므로, 오직 $p$가 참인데 $q$가 거짓일 때만 명제가 거짓입니다.

가정이 거짓인 경우($p$가 거짓)는 어떻게 해석할까요? 이 경우 결론의 참/거짓 여부와 무관하게 명제 전체는 **참**으로 간주합니다. 이는 거짓된 가정으로부터는 논리적으로 어떤 결론도 도출 가능하다는 원리(vacuous truth)를 반영합니다.

## 한 줄 예

"$x$가 6의 배수이면, $x$는 2의 배수이다" $(p \to q)$는 참인 명제입니다. 반면 "정수 $x$가 3의 배수이면, $x$는 6의 배수이다"는 거짓 명제입니다 ($x=3$일 때 가정은 참이나 결론이 거짓).
