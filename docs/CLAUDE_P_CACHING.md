# `claude -p` 프롬프트 캐싱 가이드

배치/루프에서 `claude -p`(Claude Code 비대화 모드)를 쓸 때 **프롬프트 캐싱을 살리는 법**. 헬퍼: `web/scripts/lib/claude_p.mjs`.

## 결론 (실측, 2026-06-23)

`claude -p`도 캐싱은 **된다**. 같은 프롬프트로 5분 안에 다시 부르면 base(도구+내장 시스템, ~20k~50k토큰)가 `cache_read`로 잡힌다. **문제는 캐시를 깨는 두 요인:**

1. **git status env 블록** — Claude Code 가 시스템 프롬프트에 cwd 의 git 상태를 박는다. 레포 안에서 **미커밋 변경이 다발**이면 이 블록이 비대(~17k토큰)해지고 호출 사이 계속 바뀌어 **매 호출 재기록**된다.
2. **커스텀 `--system-prompt` 는 CLI 가 캐시 안 함** (내장 base 만 캐시).

### A/B 실측 (sonnet 검증 프롬프트, 동일 프롬프트 2연속)

| cwd | 2번째 호출 cache_write(재기록) | 비고 |
|---|---|---|
| 레포(미커밋 변경 다발) | **~17,800** | 안 줄어듦 → 매번 낭비 |
| 깨끗한 빈 dir(/tmp) | **~1,115** | 정착 → 거의 cache_read |

→ **콜당 ~17k 토큰, 입력비용 ~76% 차이.** (write 1.25배 vs read 0.1배)

## 처방

1. **깨끗한 cwd 에서 실행** (가장 큰 효과). 레포 말고 빈 디렉터리에서 `claude -p` 를 spawn. 파일 접근은 `--add-dir <절대경로>` + 프롬프트에 절대경로로. → `web/scripts/lib/claude_p.mjs` 가 `/tmp/claude_p_clean` cwd 로 강제.
2. **고정 지시문은 `--system-prompt`, 가변부는 user 프롬프트** — 고정 prefix 안정화.
3. **5분 TTL 안에 연사** — 느린 루프는 캐시 증발. 호출을 몰아서.
4. **검증**: `--output-format json` 의 `usage.cache_read_input_tokens > 0` 확인.
5. 완전 제어가 필요하면 **API/SDK 직접** — cache_control 을 prefix 전체에 박아 거의 100% read.
6. **로컬 모델(맥북 gemma)** 은 토큰 0 이라 캐싱 무의미 → 대량 작업은 로컬 우선([[GEMMA_SERVER]] 참고).

## 적용 현황

- `verify_batch.mjs` (sonnet 검증기): `cwd: CLEAN_DIR` 적용 — 콜당 ~17k 회복.
- 신규 스크립트: `lib/claude_p.mjs` 의 `claudeP()` 사용.
- 미적용(추후): `gen_daily_illustration.mjs`, `api/regenerate-body.ts` (claude spawn) — 같은 패턴(clean cwd) 적용 가능.
