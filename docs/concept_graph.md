---
sources: []
created: 2026-05-16
updated: 2026-05-16
auto_generated: true
generator: D12 JIT script (regenerates from all concept frontmatter)
---

# 🕸️ Concept Dependency Graph

이 파일은 모든 concept spoke의 `prerequisites:` / `enables:` frontmatter를 **JIT 스크립트가 파싱해 regenerate**한다. 직접 수정하지 말 것. 노드 색은 mastery (D13)를 나타낸다.

> **Color legend** (Mermaid `classDef` 적용 예정):
> - 🟥 `unknown` — 아직 학습 안 함
> - 🟧 `learning` — 학습 중
> - 🟩 `proficient` — 평가원 4점 2회 통과
> - 🟦 `mastered` — 킬러 1회 통과 + 90일 무강등

---

## DAG

```mermaid
graph TD
    %% 빈 그래프 — 첫 concept 시드 후 librarian이 regenerate
    placeholder["(no concepts yet)"]
    classDef unknown fill:#fee,stroke:#c33
    classDef learning fill:#ffd,stroke:#cc3
    classDef proficient fill:#dfd,stroke:#3c3
    classDef mastered fill:#ddf,stroke:#33c
    class placeholder unknown
```

---

## Integrity Status

| Check | Result | Last Verified |
| :--- | :--- | :--- |
| Acyclic (no cycles) | ✅ trivially ok | 2026-05-16 |
| Bidirectional matching (`A.prereq ↔ B.enables`) | ✅ trivially ok | 2026-05-16 |
| Orphan concepts (no prereq, no enables, no problem ref) | 0 | 2026-05-16 |

---

## Topological Order (학습 권장 순서)

*(empty — first concepts seed needed)*

---

## 🔗 Navigation
- **Concepts Hub**: [hubs/concepts.md](hubs/concepts.md)
- **Index**: [index.md](index.md)
