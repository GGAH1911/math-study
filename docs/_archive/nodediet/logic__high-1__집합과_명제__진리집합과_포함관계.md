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

# 진리집합과 포함관계

## 정확한 진술

명제 $p(x)$의 **진리집합**은 $p(x)$를 참으로 만드는 모든 $x$의 집합입니다. 보통 $\{x \mid p(x)\}$로 표기합니다. 두 명제 $p(x)$, $q(x)$에 대해, $p(x)$의 진리집합이 $q(x)$의 진리집합에 포함될 때, 명제 "$p(x) \Rightarrow q(x)$"가 참이라고 합니다. 즉, $\{x \mid p(x)\} \subseteq \{x \mid q(x)\}$이면 $p(x) \Rightarrow q(x)$입니다.

## 직관/기하적 의미

진리집합은 명제를 "집합의 언어"로 번역하는 다리 역할을 합니다. 명제 $p(x) \Rightarrow q(x)$는 "모든 $x$에 대해 $p(x)$이면 $q(x)$"라는 뜻인데, 이것은 정확히 진리집합의 포함관계 $\{x \mid p(x)\} \subseteq \{x \mid q(x)\}$와 일치합니다. 벤다이어그램으로 생각하면, $p(x)$를 만족하는 점들의 집합이 $q(x)$를 만족하는 점들의 집합 안에 완전히 들어가 있다는 의미입니다. 이 관점을 이용하면 명제의 참/거짓을 집합 포함관계로 판정할 수 있어, 복잡한 논리를 시각적으로 이해할 수 있습니다.

## 한 줄 예

명제 "$x > 2 \Rightarrow x > 0$"는 참입니다. 왜냐하면 진리집합으로 표현하면 $\{x \mid x > 2\} = (2, \infty) \subseteq (0, \infty) = \{x \mid x > 0\}$이기 때문입니다. 반대로 "$x > 0 \Rightarrow x > 2$"는 거짓인데, 이는 $(0, \infty) \not\subseteq (2, \infty)$이기 때문입니다.
