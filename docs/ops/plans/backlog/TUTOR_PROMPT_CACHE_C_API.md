---
created: 2026-06-28
updated: 2026-06-28
status: BACKLOG
priority: P2
owner: "@insung + 튜터"
---

# 튜터 프롬프트 캐싱 C — Anthropic API 직접(cache_control)

> 프로덕션용 *추가 정밀제어*. B(CLI)가 이미 staticPrefix 를 캐싱하므로 C 는 필수가 아니라 증분 이득. [[project_claude_p_caching]]

## Context — ★정정(2026-06-28): CLI 도 `--system-prompt` 를 캐싱한다
- 이전 전제 "**CLI 는 우리 프롬프트 캐싱 불가(breakpoint 끝에만)**"는 **오류**였다(git churn 켜진 측정의
  오판, [[prompt-caching]] §2). clean cwd + DISABLE_GIT 로 prefix 안정 시 CLI 가 `--system-prompt` 를 prefix 캐싱한다.
- **e2e 실측**: chat.ts staticPrefix 를 slug-only 로 고정 후, 같은 개념 2턴(질문만 변경) → 턴1 cc=23256 →
  **턴2 cr=21720**(개념 본문 캐시 재사용). 즉 B(CLI)로 정적부 캐싱은 이미 된다.
- **C 의 역할이 바뀜** = "캐싱 가능케 하는 유일 해법"이 아니라 **증분 정밀제어**:
  ① dynamicSuffix(질문별 개념후보)에도 2번째 cache_control → 유사 질문서 동적부까지 캐시
  ② 다중 breakpoint·BYOK 모델별 cache_control ③ 자가호스팅(API 직결)은 어차피 iPad 출시에 필요([[project_ipad_app]]).

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
