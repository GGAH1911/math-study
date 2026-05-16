# 📝 Operation Log

> Append-only. Every Ingest, Merge, Prune, and Lint operation is recorded here.
> Format: `## [YYYY-MM-DD] operation | Subject`

This file is the chronological backbone of the wiki. Even when pages are deleted (Pruned), the fact that they existed and why they were removed is preserved here. The Agent appends entries; the Human reads them to understand the wiki's evolution.

---

<!-- Entries below this line. Do not edit above. -->

## [2026-05-16] init | LWIP starter kit installed; customized for math-study (Chapter 7 D1-D16); seeded hubs: concepts/problems/tools/mistakes; concept graph + learning paths + graphics pipeline (KaTeX/Mermaid/matplotlib JIT + TikZ escape, no Manim) ready. Source: 대한민국 수능·평가원·교육청 기출. Postgres ingest는 후속 작업.

## [2026-05-16] smoke | seed | 3 concepts (극한 / 미분계수 / 도함수) — bidirectional prerequisites/enables, mastery 분포 unknown:2 / learning:1. concept_graph.md regenerated (DAG depth=2, 0 cycles, 0 broken edges).

## [2026-05-16] smoke | D11+D16 L3 | matplotlib JIT generated docs/assets/미분계수/tangent_secant.svg (+ .py). sympy verified f'(1) = 2 via 한계 정의 직접 평가.

## [2026-05-16] smoke | D14 | fake problem (tangent_secant_smoke) + fake mistake (smoke_d14_gap_detection) created. Gap Detection reverse-BFS correctly identified 극한 (depth=1, mastery=unknown) as root hole over 미분계수 (depth=0, mastery=learning).

## [2026-05-16] env | added project-local .venv (uv) with sympy 1.14 + matplotlib 3.10 + numpy 2.4; .gitignore + requirements.txt updated.

## [2026-05-16] init | web/ Astro 5 + Tailwind v4 + React + react-flow scaffold. 13 pages (dashboard / fullscreen DAG / concepts·problems·mistakes·tools list+detail / paths / log). docs/ remains SSOT; web reads via content collections. SVG assets synced docs/assets/ → public/assets/ at build. Initial production build = 2.2MB, all routes HTTP 200, KaTeX/Mermaid/SVG render verified.

## [2026-05-16] deploy | exposed dev server via Tailscale. Astro bound to 0.0.0.0:4321 (HTTP via tailnet IP). Added `tailscale serve --https=8443 http://127.0.0.1:4321` for HTTPS at tme-laptop.tailf47aa4.ts.net:8443. astro.config.mjs allowedHosts includes `.ts.net` and the specific tailnet. Existing :8000 serve preserved.

## [2026-05-16] curriculum | Phase 1 concept skeleton 시드. 중1(8)+중2(8)+중3(7)+고1(6)+수학Ⅰ(4)+수학Ⅱ(3)+확률통계(3) = 39 unit 노드 + 기존 미적분 정의 3개 = **42 nodes, 62 edges, 0 cycles**. 사용자 현재 위치(이차방정식)~목표(수학Ⅱ 미분)까지 한 그래프로 연결. agent.md D3에 `unit` concept_type + `grade`/`unit`/`subunit` frontmatter 추가. web 스키마/DAG/concepts list 모두 학년별 그루핑·필터 지원. 모두 mastery=unknown(미분계수만 learning) — D14 gap detection의 토양 마련.

## [2026-05-16] feat | 단원별 LLM 튜터 채팅창 추가. 각 `/concepts/<slug>` 페이지 하단에 ChatPanel(React island) 통합. 백엔드는 Astro hybrid SSR + Node adapter, `/api/chat`이 `claude -p --output-format stream-json --include-partial-messages`를 subprocess로 spawn해 토큰 스트리밍 SSE로 프록시. 시스템 프롬프트에 페이지 본문+선수 단원 학습목표+사용자 mastery 전체+Chapter 7 D1-D16 거버넌스 자동 주입(~3-5k 토큰, prompt cache hit 시 재사용). 모델은 haiku/sonnet 토글 가능. 대화 영구화 = localStorage(`math-study:chat:<slug>`), 좋은 답변은 'Promote' 버튼으로 `/api/promote` → `docs/syntheses/<date>_<slug>_<title>.md` 영구 wiki 노드로 저장(LWIP Query & Promote, lifecycle.md §Query-Promote). API key 별도 관리 불필요 — 사용자 Claude Code OAuth 그대로 사용.

## [2026-05-16] feat(chat) | 컨텍스트 가드 추가. system prompt에 "대화 범위" 섹션: 수학·시험전략·수학자 일화·학습법 허용, 연예인/게임/정치/개인상담 거부. 거부 형식 — 한 줄 + 단원 질문 제안. 검증: 점심 추천 거부, 가우스 일화 허용, 오답노트 정리법 허용, BTS 앨범 거부.

## [2026-05-16] curriculum(complete) | **Phase 1+2+3 완전 시드** (사용자 "남은 모든 단계 다 실행" 요청). 추가 작업:
  - **선택과목 단원 추가** (Phase 1 확장): 미적분 7개(수열의극한, 여러가지함수의극한·미분, 합성함수의미분, 도함수의활용심화, 여러가지적분법, 정적분의활용) + 기하 3개(이차곡선, 평면벡터, 공간도형과공간벡터) = **49 units 총**
  - **Phase 2 spokes**: 모든 단원의 정의/정리/예제 시드. 정의 115 + 정리 102 + 예제 124 = **341 spokes**. 본문은 stub (페이지 채팅에서 학습 시 채움).
  - **Phase 3 진단 problems**: 단원당 2개씩, 자체-진단 출처로 **98 problem stubs** (단원당 2 × 49 + 기존 smoke 1 = 99). 본문은 평가원 기출 매핑 또는 자체 출제로 학습 시 채움.
  - **grade enum 확장**: `미적분`, `기하` 추가 (web schema + ConceptDAG + concepts list).
  - **hub 자동 재생성**: hubs/concepts.md = 390 노드를 학년별·타입별로 정리. hubs/problems.md = 49 단원별로 그루핑.
  - **JIT audit 통과**: ✅ 0-Isolation (490 spokes 모두 hub 또는 concept 페이지에서 inbound), ✅ DAG 양방향 매칭 (417 edges), ✅ Acyclic.
  - 결과 **390 concept nodes + 99 problem nodes + 1 mistake**. Mastery 모두 unknown(미분계수 learning만 예외). D14 gap detection의 토양이 한국 수능 전 범위로 깔림.
