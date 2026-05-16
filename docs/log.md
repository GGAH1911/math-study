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
