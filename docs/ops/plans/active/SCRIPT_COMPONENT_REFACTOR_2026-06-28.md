---
created: 2026-06-28
updated: 2026-06-28
status: PENDING
priority: P2
owner: "@insung + 튜터"
---

# 500줄 초과 스크립트·컴포넌트 리팩토링

> 분류: Operations / Tech-debt. 2026-06-28 조사. **전수 리팩토링은 비추천** — 1순위(ChatPanel)만 별도
> 진행하고 나머지는 "그 파일 작업할 때 곁들이기".

## Context
500줄 초과 파일 16개 식별(스크립트 8 + 컴포넌트 8). 줄 수가 곧 복잡도는 아니므로, **분리 이득 > 리스크**인
것만 선별 진행한다. 콘텐츠 렌더러는 단일책임이라 보류.

### 식별 목록
**스크립트(py/mjs)**
| 줄 | 파일 | 판단 |
|---|---|---|
| 1674 | `scripts/ingest_kice/ingest_round.py` | ○ 단계별 모듈화 가치, 자주 안 건드림 → 만질 때 |
| 991 | `scripts/build_solution_cache.py` | ○ 단계 분리 가치, 작동 중 → 만질 때 |
| 718 | `scripts/ingest_kice/hancom_decode.py` | △ PUA 디코딩 단일목적 |
| 662·574·540 | `ingest_v2.py`·`bbox.py`·`web/scripts/extract_figures.py` | △ 만질 때 |
| 519·512 | `qa_concept_figures.mjs`·`gen_concept_figures.mjs` | △ 도식 생성/QA, 만질 때 |

**컴포넌트/lib(tsx/ts)**
| 줄 | 파일 | 판단 |
|---|---|---|
| **1972** | `web/src/components/ChatPanel.tsx` | ◎ **1순위** 저위험 추출 |
| 1238·1096 | `ConceptDAG.tsx`·`chat-context.ts` | △ chat-context는 프롬프트 SSOT(분할 신중) |
| 1087·1084·754 | `Geometry.tsx`·`Graph.tsx`·`Geometry3D.tsx` | ✗ 보류 — 단일책임 렌더러, 분리 이득<리스크 |
| 585·549 | `InkCanvas.tsx`·`AtlasMap.tsx` | △ InkCanvas는 메모리 함정 많음, 만질 때만 |

## 실행 (1순위 — ChatPanel.tsx). 회귀방지=베이스라인 캡처→순수이동→타입체커검증→체크포인트 커밋.

### ✅ Step 1·2 완료 (2026-06-28, 저위험·검증 green)
- [x] `lib/chat/types.ts`(ChatMessage) + `lib/chat/persistence.ts`(load/save·DB·상수). 커밋 `82f0cf2d3`.
- [x] `lib/chat/markdown.ts`(normalizeLlmMarkup·renderMarkdown·serializeFrag·latexFromSelection). 커밋 `c759f2a3a`.
- [x] 검증: astro check 0 errors·내 파일 경고0(베이스라인 일치)·컴파일 200·**런타임 스모크**(개념/문제 페이지 200·에러0).
- **결과**: ChatPanel **1972 → 1737줄** (235줄 추출, 동작 무변).

### ⏸ Step 3 — Message 컴포넌트 클러스터 (보류·별도 세션 권고)
대상: `Message`(memo)/`MdSegment`/`QuotedChip`/`ErrorSegment`/`ChatScrollbar` + `parseGraphSegments`/
`Segment`/`sanitizeSvg`/`PromoteSpec`/`ChatModalState` → `components/chat/`.
- ★**보류 사유**: [[project_chatpanel_memo]] **memo prop 안정성 함정(2회 회귀 이력)** 의 한복판. 이 회귀는
  타입체커·컴파일로 **안 잡히고 실기기 긴-채팅 스크롤 성능으로만** 드러남 → 헤드리스 강행 금지.
- 추가 surface: 렌더러 7종 import·GraphicErrorBoundary·GraphicsTest의 `{ErrorSegment,parseGraphSegments}`
  import 경로 갱신.
- **착수 조건**: 실기기에서 긴 채팅 스크롤 성능 회귀 테스트 가능한 세션. 추출 후 prop 전달 방식 불변 유지.

## 검증 (완료 기준)
- [x] Step 1·2: astro check 0 errors, 컴파일 200, 런타임 스모크 통과.
- [ ] Step 3 착수 시: 긴 채팅 스크롤 끊김 없음(memo 유지) — 실기기 — [[project_chatpanel_memo]].
- [ ] 인용·검증숨김·복붙 등 기능 회귀 0(DB 검증).

## 비고
- 2~N순위(ingest_round 등)는 **별도 착수 안 함** — 해당 파이프라인 작업 시 곁들여 분리.
- 렌더러(Geometry/Graph/ConceptDAG)는 **건드리지 않음** 권장.
