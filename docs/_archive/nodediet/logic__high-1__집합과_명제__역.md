---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 논리
grade: 고1
prerequisites: [docs/concepts/logic/high-1/집합과_명제.md]
enables: []
mastery: unknown
---

# 역

조건명제 $p \to q$에서 가정과 결론을 서로 맞바꾼 명제 $q \to p$입니다. 고1 집합과 명제 단원의 기본 변환 중 하나입니다.

## 정의

조건명제 $p \to q$의 **역**은 $q \to p$입니다. 진리표 관점에서 원명제와 역은 진리값이 같지 않을 수 있으며, 다음 관계가 성립합니다.
- 원명제 $p \to q$ ⟷ 대우 $\sim q \to \sim p$: 항상 동치.
- 역 $q \to p$ ⟷ 이 $\sim p \to \sim q$: 항상 동치.
- 원명제와 역: 일반적으로 무관.

특히 원명제와 역이 모두 참이면 $p$와 $q$는 서로 동치($p \iff q$)이며, 이때 $p$는 $q$의 필요충분조건입니다.

## 예시

명제 "$x > 2$이면 $x > 1$이다"는 참입니다. 그 역 "$x > 1$이면 $x > 2$이다"는 반례 $x = 1.5$가 있으므로 거짓입니다.

반면 명제 "두 삼각형이 합동이면 두 삼각형의 넓이가 같다"는 참이지만, 역 "두 삼각형의 넓이가 같으면 두 삼각형은 합동이다"는 거짓입니다. 같은 넓이를 가지면서 모양이 다른 삼각형이 존재하기 때문입니다.

## 관련 개념

- [명제의 역](docs/concepts/logic/high-1/집합과_명제/명제의_역.md)
- [대우](docs/concepts/logic/high-1/집합과_명제/대우.md)
- [조건명제](docs/concepts/logic/high-1/집합과_명제/조건명제.md)
- [집합과 명제](docs/concepts/logic/high-1/집합과_명제.md)
