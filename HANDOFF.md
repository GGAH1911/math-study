# 핸드오프 — 2026-06-06 세션 (워크트리 gallant-tu-2c9be7)

## 🔴 지금 백그라운드로 돌고 있는 것 (셧다운 후에도 계속됨)

**솔버 백필** — `scripts/backfill_solvers.py` · **Haiku-only**(에스컬레이트 X) · setsid 분리 → 셧다운과 무관하게 자동 완주.
- 마지막 관측: **459/980** (SOLVER 400 / KEEP-GOLD 59, ~87% 성공)
- 로그: `/tmp/ingest_logs/backfill_solvers.log` · 확인: `pgrep -af backfill_solvers`
- 예상 완료: 관측 시점 +15~25분
- ⚠️ **완료 전 git 커밋 금지** — md의 `verifier:` 필드 + `db/solutions/*.py`를 계속 쓰는 중(부분커밋 위험)
- 죽으면 재개(이미 솔버 있는 건 자동 스킵): 
  `cd <worktree> && setsid env REROLL=2 .venv/bin/python scripts/backfill_solvers.py --parallel 16 > /tmp/ingest_logs/backfill_solvers.log 2>&1 < /dev/null &`

## ✅ 이번 세션 완료

1. **모평 가/나형 적재** — `ingest_ganah.py` 확장(모평 exam_type·session + `parse_moapyeong` 트리플릿 + 트랙별 정답파일). 2021 6·9월모평 가/나 **120문제**, 정답감사 0불일치, 풀이캐시 120/120 **FLAG 0**.
2. **범용 인제스트 디스패처** — `scripts/ingest_kice/ingest_auto.py`: taildrop 파일명 자동분류 → **엄격 스테이징**(2026 오염 차단) → 백엔드 라우팅(ganah/gyo12/v2) → 일괄 캐시·동기화. **기본 dry-run**, `--run`으로 실행. 21회차 정확 분류 검증. (교육청 고3 과목별 해설 v2_haesol은 가드로 제외 — 미검증.)
3. **솔버 명칭·개념 정정** — `scripts/CLAUDE.md`: "검증기"는 오칭, 본질은 **유사문제 재생성용 파라미터 솔버**. gold-match는 솔버 아님(객관식·단답 모두 솔버 필수). `build_solution_cache.py` **line 68** `use_verifier = with_verifier`(단답도 솔버 생성). **scipy 1.17.1 설치**(솔버 import 크래시 부류 제거 — 백필 실패의 주원인이었음).
4. **솔버 백필** (위, 진행 중).
5. **2021 9월모평 나형 13** 수동 솔버 작성 — `db/solutions/2021_9월모평_나형_13.py`, verified:true (정적분 활용, a³/6=9/2→a=3).
6. **UI 3종 (`/problems`)** — ① 2021 가/나형 선택칩+`가형 30·나형 30` 요약(problem-meta·problem-card에 가형/나형 추가) ② 썸네일 그리드→**번호·단원 리스트**(RoundDetails) ③ 필터 시 `<details>` **자동펼침 제거**(ProblemFilters).
7. **가/나형 시험모드** — `ExamRunner.tsx`에 `TRACKS`+`composed` prop. 2021 가/나형 회차는 **계열(가형/나형) 선택 → 그 트랙 30문항만**. `exam/round/[...key].astro` 타이머도 30 기준.
8. **랜덤 모의시험 교육과정별** — `exam-build.ts` 재작성: **3양식**(2028 통합형/공통+선택/가나형) + **단원→교육과정 영역 매핑**(대수/미적분Ⅰ/미적분Ⅱ/확통/기하/기초) + **난이도 슬라이더**(기초 고1혼합 ↔ 킬러). 2028=대수+미적분Ⅰ+확통(미적분Ⅱ·기하 제외, 조사로 확정). `random.astro` 양식·옵션·슬라이더 UI.

## ⏭️ 다음 세션 (재개 시 순서)

1. **백필 완료 확인**: `grep "완료 (" /tmp/ingest_logs/backfill_solvers.log` → SOLVER/KEEP-GOLD 최종 집계.
2. **커밋 + 푸시** (백필 끝난 뒤): 미커밋 **1600+** (코드 13 M + 새 파일 5 + 데이터 md/솔버 다수). 기본 브랜치면 브랜치부터. 새 파일: `ingest_auto.py`, `backfill_solvers.py`, `ingest_gyo12.py`, `scripts/CLAUDE.md`, `scripts/ingest_kice/CLAUDE.md`, `db/solutions/*.py` 다수.
3. **KEEP-GOLD 재시도** (크레딧 여유 시): Haiku가 솔버 못 짠 ~59+개를 Sonnet/Opus로. 로그서 `→ KEEP-GOLD` 슬러그 추출. `backfill_solvers.py` 루프에 에스컬레이트 추가(현재 'haiku' 고정)하거나 별도 런.
4. **solved_by 파일럿 계획** — `~/.claude/plans/floofy-forging-hopcroft.md` (난이도 지표=`solved_by` 신호, Phase 0 토큰 실측, **미시작**). 별개 트랙.

## 운영 메모

- **dev 서버**: 🟢 `server.sh` (PID 388905, :4323). setsid+watchdog로 Claude와 분리 — **stop 금지**, `bash server.sh status`로만 확인 (메모리 규칙).
- **scipy**: venv에 1.17.1 설치됨. `requirements`에 박아 재현성 확보 권장.
- **솔버 백필 안전성**: additive — Haiku 실패해도 gold-match(verified:true) 유지, 절대 downgrade 안 함.
- 모델: 이 핸드오프는 Opus 4.8(1M)에서 작성. 백필은 Haiku로 돈 것.
