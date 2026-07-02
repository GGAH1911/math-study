---
sources: []
created: 2026-06-28
updated: 2026-06-28
---

# 📊 크론 실행 추적 (Cron Runs)

> docs↔code↔운영 연결. `/tmp` 로그는 휘발성(재부팅 소실)이라, 여기에 **레포 추적 가능한 다이제스트**를
> 남긴다. 자동 누적(widget 크론) + 수동 스냅샷. 00_STATUS 인덱스로 traverse 진입.

## 등록된 크론 (`crontab -l`)

| 시각(KST) | 작업 | 스크립트 | 로그(/tmp) | 캐싱 |
|---|---|---|---|---|
| 03:00 | 위젯 스펙 80건 생성·검증·커밋 | `web/scripts/widget_spec_loop.mjs` → `widget_generate.mjs` | `widget_daily.log` | Opus claude -p · clean cwd + DISABLE_GIT (`cr=` 측정) |
| 06:00·12:00 | 오늘의 개념 그림 생성 | `web/scripts/gen_daily_illustration.mjs 0` | `daily-illustration.log` | haiku claude -p · clean cwd + DISABLE_GIT |
| 23:40 | 내일치 그림 미리생성(0 1 2) | `gen_daily_illustration.mjs 0 1 2` | `daily-illustration.log` | 〃 |
| @reboot | agy keepalive | `web/scripts/agy_keepalive.sh` | — | — |

## 확인법
- 위젯: `tail -40 /tmp/widget_daily.log` — `종료: accept N·skip M·합격률 X%` + `cache_read=K`(이젠 로그에 남음).
- 그림: `tail -25 /tmp/daily-illustration.log` — `완료: 생성·스킵·실패·캐시 총 N`.
- 프롬프트 캐싱 셋업: 두 스크립트 다 `cwd: CLEAN_DIR` + `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`(git churn 차단 → prefix 안정 → cache_read 생존). [[project_claude_p_caching]]

---
## 🔗 지식망 연결
- **상위 분류**: [[00_STATUS]]

## 📊 실행 로그 (자동 누적 — 최신이 아래)
| 일시(KST) | 작업 | 결과 | cache |
|---|---|---|---|
| 2026-06-28 04:03 | widget | accept 80 · skip 0 · 100% | (cr 미기록 — 이번 픽스 전) |
| 2026-06-28 06:00 | illust | 실패 0 · day+2 미리생성 | 캐시 총 26 |
| 2026-06-29 04:15 | widget | accept 80 · skip 0 · 100% | cr avg 14118 · max 18099 (n=81) |
| 2026-07-01 08:35 | widget | accept 1 · skip 0 · 100% | cr avg 14647 · max 14647 · Σcr 14647 · Σcc 3983 · save≈$0.06 (n=1) |
| 2026-07-02 03:45 | widget | accept 80 · skip 0 · 100% | cr avg 15309 · max 19353 · Σcr 1408448 · Σcc 369795 · save≈$5.88 (n=92) |
| 2026-07-03 03:35 | widget | accept 79 · skip 1 · 99% | cr avg 16825 · max 19349 · Σcr 1615226 · Σcc 239804 · save≈$6.97 (n=96) |
