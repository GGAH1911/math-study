---
created: 2026-06-28
updated: 2026-06-28
status: DONE
priority: P1
owner: "@insung + 튜터"
---

# 프롬프트 캐싱 위생 전수 반영 (clean cwd + DISABLE_GIT)

> 분류: Operations / LLM. SSOT = [[prompt-caching|docs/architecture/prompt-caching.md]].
> 전제(작성 당시): claude CLI는 우리 프롬프트 prefix 캐싱 불가 → 이 위생은 내장 base 캐시 보호.
> ⚠️★정정(후속): 이 전제는 **오판**이었다 — CLI 는 `--system-prompt` 도 prefix 캐싱한다(e2e cr=21720).
> 단, 이 위생(clean cwd + DISABLE_GIT) 자체는 **여전히 옳고 필수**(prefix 안정의 전제조건). prompt-caching.md §2.

## Context
2026-06-28 전수 조사로 누락 다수 발견(권위 문서 §5보다 많음). 표준 처방 = `cwd: CLEAN_DIR`(벨트) +
`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`(멜빵) 둘 다. 수정은 기계적·저위험(동일 패턴).

## 실행 (영향 큰 순)

### P0 — 라이브/공용/둘 다 없음
- [x] `scripts/ingest_kice/run_stage1.py` `claude_p()` — _CLEAN_DIR cwd + _CLAUDE_ENV(DISABLE_GIT) 추가
- [x] `web/src/pages/api/regenerate-body.ts` — env 에 DISABLE_GIT 추가(clean cwd 는 이미 있음)
- [x] `web/scripts/lib/claude_p.mjs` — spawn env 에 DISABLE_GIT 추가(공용 래퍼 footgun)

### P1 — 반복 배치
- [x] `web/scripts/qa_concept_figures.mjs` — CLAUDE_SPAWN(cwd+env) 공용화, claude 2곳·agy(무해) 적용
- [x] `web/scripts/verify_corrected.mjs` — cwd + env
- [x] `scripts/ingest_kice/ingest_round.py` — cwd=_CLEAN_DIR 추가(멜빵은 이미 있음)
- [x] `scripts/fill_spoke_bodies.py` — import os + cwd + env
- [x] `scripts/regenerate_searchable.py` — cwd + env

### P2 — 비전/매핑/저빈도 (★전부 공용함수 경유 → P0/P1로 자동 해결)
- [x] `concept_remap.py` → `run_stage1.map_problem` 경유 (P0-1 수정으로 해결)
- [x] `text_meta.py`·`vision_meta.py`·`crop_with_llm.py`·`llm_solve_geomgo.py` → `ingest_round.claude_p` 경유 (P1 ingest_round cwd 추가로 해결)
- 교훈: 공용 함수(run_stage1.claude_p, ingest_round.claude_p) 2개 수정이 하위 5개 동시 해결. 직접 spawn 추가 불필요.

### 문서
- [ ] `docs/architecture/prompt-caching.md` §5 표 정정 — ingest_round belt 누락 명기 + Python 누락(run_stage1 등) 반영

## 검증
- [x] py 4개 py_compile OK · mjs 3개 node --check OK · ts 는 pre-push astro check 0 err
- [x] 실측(§6-b): clean cwd+DISABLE_GIT+Read 2콜 — 1콜 cc=22939/cr=0, 2콜(다른 질문) **cr=14877 생존** = 내장 base 히트 확인(문서 측정값과 일치)

## 상태: DONE (2026-06-28). P0·P1 코드 보강 + P2 공용함수 경유 자동해결 + 문서 §5/§7 정정 + 실측 검증 완료.
