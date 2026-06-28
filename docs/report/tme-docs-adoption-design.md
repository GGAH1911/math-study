# TME docs 방식 이식 설계안 (math-study)

> 결정 전 검토용. TME(부동산포렌식) docs 시스템의 **handover + plans 생애주기 + (선택)자동인덱스**를
> math-study에 이식하는 구체 설계. **콘텐츠 메시(concepts·problems, audit-lwip 거버넌스)는 건드리지 않음.**

---

## 0. 원칙 — 무엇을 바꾸고 무엇을 안 바꾸나

| 영역 | 현재 | 이 설계 |
|---|---|---|
| **콘텐츠 메시** (`docs/concepts` · `docs/problems` · `hubs`) | audit-lwip 거버넌스, entropy=0, 단일 DAG | **그대로 둔다** (이미 안정) |
| **세션 인계** (`docs/HANDOFF.md`) | 단일 롤링 파일(64줄, 덮어씀) | → `docs/handover/` 디렉터리(세션별) |
| **계획** (`docs/TODO.md`) | 단일 파일(133줄) | → `docs/ops/plans/` 생애주기 |
| **개발문서** (`architecture`·`report`·`audits`·낱개 md) | 평면 | (선택) 자동 00_인덱스 |

---

## 1. Handover — 세션별 인계 (HANDOFF.md 대체)

### 폴더
```
docs/handover/
├── 00_HANDOVER.md              ← 인덱스(규약 + 최신 링크)
└── 2026/
    └── 06/
        ├── 28_session.md       ← 하루 1파일, 세션마다 블록 이어붙임
        └── 27_session.md
```

### 파일 스키마 (`YYYY/MM/DD_session.md`)
```markdown
---
date: 2026-06-28
sessions: 2
open_questions: 3
---

# 2026-06-28 Handover

## 🕒 세션 04:30
> 집도: 튜터 채팅 UX 라운드
**총평**: <1-2줄>
### 🚀 주요 성과
- <불릿, [[wikilink]] 가능>
### 🚦 현재 상태·잔류 리스크
- <비차단 미반영 등>
### 📝 차기 과제 (Next — start here)
- <구체 첫 행동>

(다음 셧다운 시 '## 🕒 세션 [시각]' 블록을 아래에 이어붙임)
```

### Boot/Shutdown 통합 (우리 "부팅/셧다운" 관행에 맞춤)
- **부팅 시**: 최신 handover의 **차기 과제 + 미해결 질문**을 먼저 읽고 보고.
- **셧다운 시**: 오늘자 파일에 세션 블록 **append**(덮어쓰기 X). 조용한 세션도 1줄 기록.

---

## 2. Plans — 계획 생애주기 (TODO.md 대체)

### 폴더
```
docs/ops/plans/
├── 00_PLANS.md                 ← 인덱스
├── active/                     ← 진행 중 (지금 하는 것)
│   └── 00_ACTIVE.md
├── pending/                    ← 착수 대기 (다음 후보)
├── backlog/                    ← 장기·아이디어
├── completed/2026_06/          ← 완료(월별 아카이브)
└── reference/                  ← 로드맵·설계 SSOT(상태 없는 영구 참조)
```

### plan 문서 스키마 (`<TOPIC>_2026-06-28.md`)
```markdown
---
created: 2026-06-28
updated: 2026-06-28
status: ACTIVE          # ACTIVE | PENDING | BACKLOG | DONE
priority: P1            # P0 긴급 · P1 중요 · P2 일반
owner: "@insung + 튜터"
---

# <계획 제목>
## Context  — 왜·배경
## 실행 — 단계/체크박스
## 검증 — 완료 기준
```

### 생애주기 규칙
- 착수 → `active/`. 완료 → frontmatter `status: DONE` + **`completed/2026_MM/`로 이동**.
- TODO.md의 "후속작업"은 plan 문서로 승격하거나 backlog로.

---

## 3. (선택) 자동 인덱스 — `00_<DIR>.md`

TME `ensure_wiki_indices.py` 포팅. **개발문서 영역에만 적용**(콘텐츠 메시 제외):
- 대상: `docs/handover`·`docs/ops`·`docs/architecture`·`docs/report`·`docs/audits` 등.
- **제외**: `docs/concepts`·`docs/problems`·`docs/hubs`·`docs/mistakes`·`docs/notes`·`docs/syntheses`·`docs/paths` (콘텐츠 = audit-lwip 관할).
- 동작: md 있는 폴더에 `00_<DIR>.md`(전수 명세 + 상위 링크) 없으면 생성, `<!-- AUTO_INDEX_SECTION -->` 갱신.
- 실행: `web/package.json` prebuild/predev 체인 끝에 `node scripts/ensure-doc-indices.mjs` 추가(audit-lwip와 병렬).

---

## 4. 우리 메모리 시스템과의 역할 분담 (★중요)

| | 위치 | 수명 | 용도 |
|---|---|---|---|
| **memory** (`~/.claude/.../memory/`) | 레포 밖 | 영구·세션간 | 비자명한 사실·교훈·"왜"(내가 매 세션 자동 로드) |
| **handover** (`docs/handover/`) | 레포 안(git) | 세션→다음세션 | 그 세션에 한 일·차기 행동(부팅 시 읽음) |
| **plans** (`docs/ops/plans/`) | 레포 안(git) | 계획 생애주기 | 무엇을 할지·진행상태 SSOT |

- **중복 회피**: handover는 *그 세션 서사*(휘발 방지), memory는 *교훈/패턴*(재사용), plans는 *할 일 상태*. 같은 사실을 셋에 중복 기록하지 않음 — handover에서 교훈이 나오면 memory로 승격, 할 일이 나오면 plan으로.

---

## 5. 마이그레이션 단계 (적용 결정 시)

1. `docs/handover/` 생성 + `00_HANDOVER.md` 규약 작성. 현 `HANDOFF.md` → `2026/06/28_session.md`로 이전(내용 보존), 루트 HANDOFF.md는 "→ handover/ 이전됨" 1줄 포인터.
2. `docs/ops/plans/{active,pending,backlog,completed,reference}/` 생성 + `00_PLANS.md`. 현 `TODO.md` 항목을 active/backlog/완료로 분류 이동.
3. (선택) `scripts/ensure-doc-indices.mjs` 작성 + prebuild 체인 등록.
4. `agent.md` 또는 CLAUDE 규약에 "부팅=최신 handover 읽기 / 셧다운=handover append" 1줄 추가.

**예상 비용**: 1~2단계만이면 ~30분(폴더+규약+기존파일 이전). 3단계 추가 시 +스크립트 1개.

---

## 6. 권고
- **1+2 (handover + plans)** 는 즉시 ROI 높음 — 단일파일 한계(맥락 누적소실) 직접 해결, 콘텐츠·거버넌스 무영향.
- **3 (자동인덱스)** 는 개발문서가 더 늘면 그때. 지금은 낱개 md 십수 개라 수동으로도 충분.
- **전체 토폴로지 전환(콘텐츠까지)** 는 비추천 — 현 허브 시스템이 이미 entropy=0.
