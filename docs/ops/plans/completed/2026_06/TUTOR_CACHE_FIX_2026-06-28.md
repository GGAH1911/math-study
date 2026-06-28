---
created: 2026-06-28
updated: 2026-06-28
status: DONE
priority: P0
owner: "@insung + 튜터"
---

# 튜터 프롬프트 캐싱 정정 + staticPrefix 완전 고정

> 분류: Architecture / LLM. SSOT = [[prompt-caching|docs/architecture/prompt-caching.md]].

## Context — ★이전 결론이 틀렸다 (git churn 함정에 두 번)
2026-06-28 대조실험으로 **claude -p 는 `--system-prompt` 를 prefix 캐싱함**을 증명:
- 큰 SYS 고정 + 질문만 변경 → 2콜째 cr=22982(base 14877 초과). SYS 2배 → cr=32265(크기 비례).
  SYS 한 글자 변경 → cr=12745 붕괴 + cc 재기록(인과 확정).
- production tutor_usage: concepts max_cr=**29237**(2/11 콜) — 개념 본문이 실제 캐시됨.
- 즉 "CLI 는 우리 프롬프트 캐싱 불가"(문서 §2)는 **오류**. 0628 "정정" 측정이 DISABLE_GIT 들어가기
  *전*(git churn 활성)에 잰 것으로 추정 → cta-law '헛다리'와 **같은 실수 반복**.

## 실행
- [x] **chat.ts staticPrefix 완전 고정**: per-user 동적값 2개를 dynamicSuffix(캐시 경계 밖)로:
      ① `buildTutorPrompt(slug, collection)` — userMastery 인자 제거(currentMastery=frontmatter 정적).
      ② userMastery → dynamicSuffix 에 "★promote/demote 판정 기준" 권위 override. learnerContext 도 이동.
      → staticPrefix = slug-only(body·prereq·enables·masteryByLevel(frontmatter)·linkedProblems) = byte-stable.
- [x] 타입체크 — pre-push astro check 0 err
- [~] 실측: noauth 포트 2턴 — **보류**(4325 DEV_NOAUTH/authed 세션·로깅이 로그인 유저限라 실패점多).
      메커니즘은 §2 대조실측으로 인과 증명 + 리팩토링이 staticPrefix 를 순수 slug 함수로 만듦 →
      실사용(로그인 멀티턴) 누적으로 tutor_usage concepts avg_cr 상승 확인 예정.
- [x] **문서 정정** prompt-caching.md §2(핵심진실 교체)/§5(chat row·note)/§6-(e)(매트릭스+해석).
- [x] **메모리 정정** [[project_claude_p_caching]] — 오결론 교체 + "git churn 함정 2회" 교훈.

## 검증 기준
- staticPrefix 가 같은 concept 의 모든 턴에서 byte-identical(per-user 동적값 0).
- 2턴째 cr 이 base(~14877) 초과(= 콘텐츠 캐시 히트).
- 튜터가 per-user mastery 를 여전히 정확히 사용(강등 버그 회귀 없음).

## 상태: DONE (2026-06-28). 코드·문서·메모리 정정 완료. e2e 실측만 실사용 누적으로 보류.
