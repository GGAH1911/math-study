---
created: 2026-06-28
updated: 2026-06-28
status: ACTIVE
priority: P1
owner: "@insung + 튜터"
---

# TME docs 방식 이식 (handover + plans + 자동인덱스)

> 분류: Operations / Docs. 설계 SSOT = `docs/report/tme-docs-adoption-design.md`. 선택지 ② 채택.

## Context
TME(부동산포렌식) docs 시스템의 세션관리 패턴을 math-study에 이식. GitHub LWIP은 범용·허브·생성코드0이라
TME의 per-directory 자동인덱스·plans 생애주기는 미포함 → 우리 프로젝트에 직접 이식. **콘텐츠 메시
(concepts·problems, audit-lwip)는 무영향.**

## 실행
- [x] `docs/handover/` 골격 + `00_HANDOVER.md` 규약. HANDOFF.md → `2026/06/27_session.md` 이전 + 루트 포인터.
- [x] `docs/handover/2026/06/28_session.md` (오늘 세션) 작성.
- [x] `docs/ops/plans/{active,pending,backlog,completed/2026_06,reference}/` 골격 + `00_PLANS.md` 규약.
- [x] TODO.md 분류 이전(open→backlog, 완료이력→reference 아카이브, 루트 포인터).
- [x] `scripts/ensure-doc-indices.mjs` 작성 — 개발문서 폴더에 `00_<DIR>.md` 자동생성/갱신.
      AUTO_INDEX_SECTION만 재생성(수동 설명 보존), 콘텐츠 폴더 제외.
- [x] `web/package.json` prebuild/predev 체인에 등록(audit-lwip 뒤).
- [x] 첫 실행 → 개발문서 폴더 11개 인덱스 생성, 콘텐츠 폴더 0개(제외 확인), 멱등성 확인.

## 검증
- [x] 콘텐츠 폴더(concepts/problems/hubs)엔 00_ 인덱스 **안 생김**(0개) — 제외 정상.
- [x] 멱등성: 재실행 시 created/updated 0(수동 설명 보존).
- [ ] 부팅 시 최신 handover의 차기과제가 읽히는지(다음 세션 실증) — **남은 검증**.
- [ ] 다음 build에서 audit-lwip 회귀 0 확인(콘텐츠 메시 무영향).

## 상태: 골격·스크립트 완료. 다음 세션 부팅 실증 후 DONE → completed/2026_06 로 이동.
