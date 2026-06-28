---
date: 2026-06-28
sessions: 1
open_questions: 2
---

# 2026-06-28 Handover

## 🕒 세션 (튜터 채팅 UX 라운드 + TME docs 이식)
> 집도: 튜터 검증/풀이 정확도 · 채팅 UX(스크롤·인용) · LWIP/TME docs 조사·이식

**총평**: 튜터의 검증풀이 준수(c=9 정확 유도)·검증과정 숨김·드래그 인용(표·수식 보존)을 DB 직접검증으로 완성하고, 채팅 스크롤 흔들림·재진입 바텀을 픽스. 이어 GitHub LWIP v1.6과 TME(부동산포렌식) docs 시스템을 조사해, math-study에 **handover + plans 생애주기 + 자동인덱스**(②)를 이식 시작.

### 🚀 주요 성과
- **튜터 정확도(C)**: 검증풀이 주입 준수 + 시스템 산술검산(shunting-yard, CSP-safe) + 오탐 정규식 수정. DB검증 완료(2027 6월모평 21: c=9·f(2)=11). [[project_tutor_chat_ux]]
- **검증과정 숨김(A)** + 자동검증 시스템메시지 프레이밍.
- **드래그 인용**: 선택범위만 인용, `.katex` annotation(SSOT) 직접추출 + `serializeFrag`(표→md·줄바꿈 보존) + 오버레이 하이라이트(iPad touchend 우회). DB검증 완료.
- **채팅 스크롤**: 스트리밍 흔들림(instant 전환) + 재진입 바텀.
- **수식 복붙 폴백**: 렌더 KaTeX 복붙을 인용 칩으로 마스킹.
- **LWIP/TME 조사**: GitHub LWIP=범용·허브·생성코드0(의도), TME=실전·per-directory 자동인덱스·plans 생애주기(프로젝트 고유). → TME 확장을 우리에 이식 결정(②). 설계=`docs/report/tme-docs-adoption-design.md`.
- **TME docs 이식(진행중)**: `docs/handover/` + `docs/ops/plans/{active,pending,backlog,completed,reference}/` 골격·규약 생성, HANDOFF.md→handover 이전.

### 🚦 현재 상태·잔류 리스크
- 이번 세션 채팅 UX 커밋 전부 push 완료(~`00d47cdfb` 이후 인용 라운드까지).
- 미커밋 debris(내 것 아님): `concept-illustrations.json`(일일크론)·`figrender.astro`·`goldboard.astro`.
- 서버: 4324·4325 up, 4323 down(원래 상태).

### 📝 차기 과제 (Next — start here)
1. **TME docs 이식 ② 마무리**: `docs/ops/plans/` 규약(`00_PLANS.md`)·TODO.md 항목 분류이전 · 자동인덱스 스크립트(`scripts/ensure-doc-indices.mjs`) 작성·prebuild 등록.
2. **스크립트/컴포넌트 리팩토링 검토**: 500줄 초과 8+8개 식별됨(아래 plans 또는 별도 plan). 최대=`ChatPanel.tsx` 1972줄·`ingest_round.py` 1674줄.
3. (대기) 갈무리→튜터 이미지 피드백 / 필기·그래프 DB 귀속 / 미확인 실기기 테스트(`docs/report/test-checklist-2026-06-28.md`).
