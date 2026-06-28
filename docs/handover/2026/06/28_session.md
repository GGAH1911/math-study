---
date: 2026-06-28
sessions: 2
open_questions: 3
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

---

## 🕒 세션 2 (모듈화 + 인덱싱 확장 + 캐싱 측정 + docs 정리)
> 집도: 대규모 모듈화 · 소스코드 00 인덱싱 · 프롬프트 캐싱 진실규명 · docs 루트 정리

**총평**: ChatPanel(1972→582·−70%) 및 chat-context·ConceptDAG·build_solution_cache 모듈화. 00 인덱싱을 docs→**소스코드까지 확장**(설계↔코드 traverse). 튜터 캐시를 DB 계정별 적재하며 ★"claude CLI는 우리 프롬프트 prefix 캐싱 불가"를 측정으로 규명(인제스트 cr은 내장 base였음 — **⚠️이 결론은 후속 세션에서 오판으로 정정됨: 실제로 CLI는 --system-prompt를 캐싱, 아래 §캐싱 진실 정정 참조**). docs 루트 12→3개 정리.

### 🚀 주요 성과
- **모듈화**(신규 모듈 14+): ChatPanel→lib/chat/*·components/chat/*. chat-context→tutor-rules·concept-fs. ConceptDAG→dag-types·dag-layout·ConceptNode. build_solution_cache→solve_prompts. 회귀방지=베이스라인→순수이동→타입체커→스모크→체크포인트커밋. [[feedback_module_first]]
- **소스코드 00 인덱싱**: ensure-doc-indices.mjs 다중루트(docs+web/src+scripts). 폴더명 충돌 시 부모 접두(00_LIB_CHAT). docs/architecture↔00_SRC 양방향. traverse 링크 69개 댕글링0.
- **튜터 usage DB 적재**: tutor_usage 테이블(0004)+lib/tutor-usage.ts+chat.ts result 캡처. 계정별 input/output/cache_read/creation.
- **★캐싱 진실**: claude CLI는 cache_control breakpoint를 끝에만 → 우리 프롬프트 prefix캐싱 불가. 인제스트 cr=claude 내장 base(도구정의). 도구튜터(problem)는 DISABLE_GIT로 base cr 생존(0→20585), 개념튜터(--tools'')는 미미. safeChildEnv에 DISABLE_GIT 빠져있던 것 추가. 권위문서 architecture/prompt-caching.md. [[project_claude_p_caching]]
  - **⚠️★정정(2026-06-28 후속 세션)**: 위 "prefix캐싱 불가"는 **오판**(git churn 켜진 측정). 실제로 **CLI는 `--system-prompt`를 prefix 캐싱한다** — e2e 실측 턴1 cc=23256→턴2 cr=21720(개념 본문 캐시). chat.ts staticPrefix를 slug-only로 고정해 멀티턴 cr 살림. prompt-caching.md §2 재정정 참조.
- **크론 추적**: widget_spec_loop cr 로그 + docs/ops/status/cron-runs.md 자동누적.
- **docs 루트 정리**: 낟개 7개→분류폴더, 빈 포인터 삭제, readFileSync 실경로 갱신.

### 🚦 현재 상태·잔류 리스크
- 전부 push(~8eed577ae). astro check 0 errors. 서버 4324·4325 up.
- 미커밋 debris(내 것 아님): concept-illustrations.json·figrender.astro·goldboard.astro.
- ★cache_read 0(개념 튜터)은 버그 아니라 CLI 한계 — C 필요.

### 📝 차기 과제 (Next — start here)
1. **C: 튜터 프롬프트 캐싱 API 직접**(프로덕션) — backlog/TUTOR_PROMPT_CACHE_C_API. Anthropic Messages API + cache_control breakpoint. 출시차단(자가호스팅)과 묶임.
2. **캐싱 누락 보강**(architecture/prompt-caching.md §5): claude_p.mjs·regenerate-body 등 DISABLE_GIT 추가.
3. (대기) 갈무리→튜터 이미지 피드백 / 필기·그래프 DB귀속 / 미확인 실기기 테스트(test-checklist-2026-06-28.md).
