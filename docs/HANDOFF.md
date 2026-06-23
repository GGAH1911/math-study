# 핸드오프 — 2026-06-23 · 인제스트 캐싱/루프 + 2019수능 적재 + claude -p 전수 캐싱

> **다음 세션 "부팅해" → 이 문서대로 이어받기.** 메모리 `project_solution_cache`·`project_handsolve_tiles`·`feedback_main_only_commit`·`feedback_handsolve_orchestrator` 동반 참조. (이전 도식 파이프라인 핸드오프는 아래 "이전 컨텍스트" 참고.)

## ★부팅 시 먼저 할 일
1. **상태 점검**: `git status`(깨끗해야), `git log --oneline -8`(아래 커밋 확인), `./server.sh status`(끄지 말 것).
2. **gemma 서버**: `web/scripts/gemma_server.sh status`. 인제스트/변환 안 돌면 유휴. 필요 없으면 watchdog 꺼도 됨(아래 셧다운 참조).
3. **이어받을 작업 없음(이번 세션 전부 완료·커밋)** — 새 지시 대기. 새 회차 인제스트 시 `python scripts/ingest_kice/ingest_auto.py --run`(아래 파이프라인).

## 이번 세션(2026-06-23) 한 일 — 전부 커밋·푸시됨 (bc2888ab0 까지)
1. **claude -p 프롬프트 캐싱 전수 적용** (핵심). 레포 cwd면 git-env 블록 churn으로 캐시가 깨짐 → 모든 claude -p 호출을 **clean cwd**(`/tmp/claude_p_clean`)에서 spawn. 적용 경로: verify_batch·corrector·ingest_round(claude_p)·build_solution_cache(5곳)·chat.ts(튜터)·gen_daily_illustration·regenerate-body + cta-law llm_client. 실측 콜당 cache_read≈43k·plain in~0 → 프리픽스 ~10× 절약. **개념매핑 60초 타임아웃도 해소**(거대 env 제거). 한계: 커스텀 `--system-prompt`는 CLI가 캐시 안 함(내장 base만) → 완전캐싱은 API 직접 cache_control 필요(미실행). 상세 `docs/CLAUDE_P_CACHING.md`.
2. **재교정 agent-loop 백엔드**: corrector.mjs 에 `CORR_BACKEND=agent`(claude -p `--max-turns`, 이미지 Read→교정→자가검증). agy(쿼터다운) 대체. ingest_auto `RECORRECT_BACKEND` env override. gemma 격리 하드테일 자동복구 실증.
3. **교정 후처리 배선**(ingest_auto): corrector → **box_backfill**(결정적 박스마커, LLM0) → **concept_remap**(교정된 텍스트로 개념 재매핑, '매핑前 교정' 원칙, haiku·캐시) → 솔버캐시 → sync. PAR_C 기본 2(gemma 2병렬). corrector validate 길이비에서 `[그림:]` 제외(false-positive 격리 방지)+재교정 성공시 격리마커 해제.
4. **2019학년도 수능 완전 적재**: 60문제(가/나형 각30). corrector_verify 60/60 ok·솔버 60/60·verified 60/60·박스11·개념60. **핸드솔브 9건 오케스트레이터 직접풀이**(변이테스트 ±1→FAIL 전수통과): 가형22/23/24/27/28/30·나형22/29/30. 하이라이트 **가형30(킬러)=p=-9π 닫힌형 a²=27**, 가형28(타원)=수치검증11.
5. **ad-hoc 슬러그 정리**: 개념그래프에 없는 즉석 슬러그(LLM 매핑 부산물, 전 회차 누적)를 `scripts/cleanup_adhoc_concepts.py`로 정리. 38종 기존개념 흡수(정규화+의미매핑)·1종 제거·레거시 멀티라인2건·빈concepts1건 수정. **새 개념 생성 0**(사장님 지침: 최대한 기존 노드 연결). build-problem-index에 flat-slug→nested 폴백 추가. 누락 668→**0**, 빈concepts 0, audit_solvers orphan/누락 0.
6. **핸드솔브 큐 vision_tiles 주입**: `_queue_entry`가 타일경로+instruction을 큐 json에 넣어, 오케스트레이터가 통이미지 대신 **타일을 Read로 직접** 보게 강제. scripts/CLAUDE.md 프로토콜 명시. [[project_handsolve_tiles]]

## 결정 사항 (사장님 지시)
- **gemma 솔버 도입 안 함** — 테스트 결과 상급 killer(가형30) 🔴 완전실패(답·솔버 0). 기존 사다리(Haiku→Sonnet→Opus + 오케스트레이터 핸드솔브) 유지. (난이도별 예상 하🟢/중🟡/상🔴 실증.)
- **검정고시 인제스트 안 함** (이번엔).

## 인제스트 파이프라인 (차기 회차 — 검증된 자동 흐름)
```
python scripts/ingest_kice/ingest_auto.py --run [--only <slug>]
  → 감지/스테이징 → 추출+크롭 → 교정[gemma×2 ∥ sonnet검증(캐시) ∥ 재교정]
  → box_backfill → concept_remap → build_solution_cache → post_ingest_sync
```
- 재교정 백엔드: 기본 agy. agy 다운 시 `RECORRECT_BACKEND=agent`(claude 에이전트루프).
- 솔버: auto 사다리 통과분 자동 + **단답 gold-match·killer·도형은 핸드솔브 큐 → 오케스트레이터 직접**(서브에이전트 위임 금지, [[feedback_handsolve_orchestrator]]). 큐 json `vision_tiles` 를 Read 로 보고 변이테스트 통과 솔버 작성.
- 멱등: corrector_verify:ok·skip-cached 자동 스킵.

## 커밋 정책 / 미커밋
- main-only + 작업 끝나면 commit+push. git 상태 현재 깨끗.
- 미추적 debris(내 것 아님, 건드리지 않음): `web/{scratch_tangent.png,test_*.py,verify*.py}` — 이전 세션 산물.

## 함정 (이번 세션 + 기존)
- **clean cwd 안전조건**: 파일 접근은 반드시 `--add-dir`(절대경로). 상대경로 의존 호출은 clean cwd로 옮기면 깨짐(verify 실행 `_run_code` 등은 cwd 안 바꿈).
- **build-problem-index 누락 경고**: 문제 frontmatter가 flat slug(`docs/concepts/X.md`) 참조인데 개념은 nested 저장 → leaf 유일 시 폴백. leaf 중복이면 모호로 남김.
- **레거시 멀티라인 concepts**: 구형 문제는 `concepts:\n  - 슬러그`(경로없음) 형식 — 단일라인 `[...]` 정규식이 못 잡음. 정리 시 둘 다 처리.
- **가짜솔버 방지**: 변이테스트(CANDIDATE ±1→FAIL) 필수. 객관식은 게이트 약함→realmath+원본통과만, 도형은 타일 직접보고 검증.
- gemma 상급 killer 무능(닫힌형 추론·도형판독 불가). 서버 stop 금지(setsid). 서버 뜬 채 `astro check`/`npm install`→Vite stale→`server.sh restart`. 로그 `>` 덮어쓰기 금지(append/타임스탬프).

## 이전 컨텍스트 (도식 파이프라인 — 보류, 별도 재개 시)
함수 개념도식 gen 완료(figure 450)·QA(area전수점검) 진행중이었음 → 3D(Geometry3D, 설계대기) → 기출 Gemini 교정기. 상세 [[project_concept_figures]]·[[project_gemini_corrector]]. 재개하려면 git 이력 9ad32dec6 근방 + 당시 하트비트 cron 프롬프트 참조(git log).
