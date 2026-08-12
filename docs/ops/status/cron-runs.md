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
| 2026-07-04 03:32 | widget | accept 80 · skip 0 · 100% | cr avg 16744 · max 19344 · Σcr 1557180 · Σcc 239991 · save≈$6.71 (n=93) |
| 2026-07-05 03:36 | widget | accept 78 · skip 2 · 98% | cr avg 16803 · max 19346 · Σcr 1579453 · Σcc 236647 · save≈$6.81 (n=94) |
| 2026-07-06 03:36 | widget | accept 77 · skip 3 · 96% | cr avg 16825 · max 19363 · Σcr 1615246 · Σcc 241109 · save≈$6.97 (n=96) |
| 2026-07-07 03:18 | widget | accept 48 · skip 0 · 100% | cr avg 16530 · max 19340 · Σcr 859559 · Σcc 145585 · save≈$3.69 (n=52) |
| 2026-07-08 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-09 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-10 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-11 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-12 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-13 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-14 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-15 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-16 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-17 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-18 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-19 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-20 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-21 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-22 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-23 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-24 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-25 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-26 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-27 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-28 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-29 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-30 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-07-31 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-01 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-02 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-03 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-04 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-05 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-06 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-07 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-08 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-09 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-10 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-11 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-12 03:00 | widget | accept 0 · skip 0 · 0% | cr 없음 |
| 2026-08-12 22:59 | widget | accept 0 · skip 0 · 0% | cr 없음 |
