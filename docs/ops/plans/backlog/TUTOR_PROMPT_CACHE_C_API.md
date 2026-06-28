---
created: 2026-06-28
updated: 2026-06-28
status: BACKLOG
priority: P2
owner: "@insung + 튜터"
---

# 튜터 프롬프트 캐싱 C — Anthropic API 직접(cache_control)

> 프로덕션용. B(CLI)에서 확인한 한계를 API 직접 호출로 해소. [[project_claude_p_caching]]

## Context — B에서 측정으로 밝혀진 진실
- **claude CLI(`-p`)는 우리 시스템 프롬프트를 prefix 캐싱 못 한다.** CLI 가 cache_control breakpoint 를
  프롬프트 *끝*에만 자동으로 찍어서, 전체가 byte-identical 일 때만 cache_read 히트(질문이 바뀌면 미스).
- **인제스트·배치의 "캐싱 성공"은 claude 내장 base(시스템+도구 정의)가 캐시된 것**이었다 — 우리 거대
  프롬프트가 아니라. (실측: 도구 활성 시 완전 다른 질문 2회도 cr 동일 ≈ 내장 base 토큰.)
- 그래서 **도구 쓰는 튜터(problem, --allowedTools Read)는 DISABLE_GIT 만으로 내장 base cr 생존**(실측
  cr≈20585) = 약간의 실질 절약. **개념 튜터(--tools "")는 base 가 작아 절약 거의 없음.**
- 우리 거대 시스템 프롬프트(~29k자/수천토큰)는 **CLI 로는 캐시 불가** → C 필요.

## 실행 (C)
- [ ] `/api/chat` 의 claude CLI spawn → **Anthropic Messages API 직접 호출**(SDK 또는 fetch)로 대체.
- [ ] system 을 블록 배열로: `[{type:'text', text: staticPrefix, cache_control:{type:'ephemeral'}}]` —
      staticPrefix(slug·user 고정) 끝에 명시적 breakpoint → 연속 질문서 cache_read 생존.
- [ ] dynamicSuffix(질문별 개념후보)·대화 history 는 messages 로(캐시 경계 밖, 또는 history 에 2번째 breakpoint).
- [ ] 스트리밍(SSE) 유지 + usage 의 cache_read/creation 을 tutor_usage 에 적재(이미 구현된 logTutorUsage 재사용).
- [ ] BYOK(openrouter) 경로도 동일 cache_control(지원 모델 한정).
- ★출시 차단 항목과 묶임: chat.ts 자가호스팅→API 직결([[project_ipad_app]]). API key 관리·비용 가드 필요.

## 검증
- 같은 페이지 연속 질문 2회 → tutor_usage.cache_read_tokens 가 staticPrefix 토큰만큼 상승.
- B 대비 절약률(개념 튜터에서 0 → staticPrefix 캐시분).

## B 단계 산출물(완료, 이 plan 의 발판)
- staticPrefix/dynamicSuffix 분리 구조(chat.ts) — C 에서 cache_control 찍을 자리.
- DISABLE_GIT env 추가(내장 base cr 생존) + tutor_usage 로깅(캐시 실측 인프라). 커밋 단위 git log.
