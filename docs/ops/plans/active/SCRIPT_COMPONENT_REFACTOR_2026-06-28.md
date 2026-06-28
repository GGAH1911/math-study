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

## 실행 (1순위만 — ChatPanel.tsx 1972→~600줄)
이미 내부에 독립 함수/컴포넌트가 잘 나뉘어 있어 **저위험 추출**. 단 ★메모리 `project_chatpanel_memo`
(Message memo prop 안정성, 2회 회귀 이력) 준수 — 추출해도 prop 안정성 유지.

- [ ] `lib/chat/persistence.ts` — `loadHistory`/`saveHistory`/`saveDbHistory` + STORAGE_PREFIX.
- [ ] `lib/chat/markdown.ts` — `normalizeLlmMarkup`/`renderMarkdown`/`sanitizeSvg`/`serializeFrag`/
      `latexFromSelection`/`reconstructPastedMath`.
- [ ] `components/chat/` — `Message`/`MdSegment`/`QuotedChip`/`ErrorSegment`/`ChatScrollbar` 추출
      (export 유지, import 경로만 변경).
- [ ] `ChatPanel.tsx` 는 컨테이너(state·send·effect·레이아웃)만 남김.
- [ ] 컴파일·타입체크 0 + 회귀 테스트(스트리밍·인용·검증숨김·KaTeX·memo 성능).

## 검증 (완료 기준)
- `npx astro check` 0 errors. 컴파일 HTTP 200.
- 긴 채팅 스크롤 끊김 없음(memo 유지 확인) — [[project_chatpanel_memo]].
- 인용·검증숨김·복붙 등 이번 세션 기능 회귀 0(DB 검증).

## 비고
- 2~N순위(ingest_round 등)는 **별도 착수 안 함** — 해당 파이프라인 작업 시 곁들여 분리.
- 렌더러(Geometry/Graph/ConceptDAG)는 **건드리지 않음** 권장.
