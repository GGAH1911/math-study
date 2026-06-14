# 핸드오프 — 2026-06-14 · 한컴 PUA 디코더 결정론 완성 + 전수 백필

> 다음 세션이 바로 이어받도록: 현재 상태 / 한 일 / 검증 재실행 / 남은 일 / 함정.

## 현재 상태
- **브랜치·커밋**: `origin/main` @ `de4d0a57`. 작업 worktree = `.claude/worktrees/festive-shirley-76b305` (브랜치 `claude/festive-shirley-76b305`, upstream `origin/main`, FF로 push).
- **dev 서버**: festive-shirley worktree 서빙, `0.0.0.0:4323` (setsid+watchdog 분리 — **끄지 말 것**, `server.sh status`로 확인만). http://tme-laptop.tailf47aa4.ts.net:4323 . 문제 페이지는 로그인 게이팅(비로그인 302).
- **검증 결과**: 한컴 PUA 재구성 **결정론 위반 216→6 (0.17%)**, **KaTeX 렌더실패 0/2986**. 전수 백필 적용 완료.

## 이번 세션 한 일
1. 재구성 오류 검증을 **비전감사(확률·샘플) → 결정론·전수 불변식 스캐너**로 전환 (사장님 "확률적 느낌이라 불안" 해소).
2. 디코더 **8수정으로 216→6** — 상세는 `docs/TODO.md` 완료(2026-06-14) + 메모리 `project_hancom_rosetta`.
3. **전수 백필** 3564처리/1626변경/0실패 + `.astro`/vite 캐시 클리어 + `server.sh restart`.
4. **재구성 뷰 어드민 전용** 게이팅 — 사용자는 원본 이미지만(`[...slug].astro` `reconHTML = isAdmin ? reconFull : ''`).

## 검증 재실행 (결정론·전수·LLM무관)
- `scripts/ingest_kice/qa_invariant_scan.py` — 구조 불변식(PUA잔존·중괄호불균형·overline숫자·표garble·빈구조·footer/doubling·구분선·이중첨자). 입력 `/tmp/vision_qa/decoded_all.jsonl`.
- `scripts/ingest_kice/qa_rawleak_scan.mjs` — 전 문제 KaTeX 렌더 후 raw-latex 누출(파싱실패). 입력 동일 + `/tmp/recon.mjs`.
- `scripts/ingest_kice/qa_glyphs_for.py <id>` — 문제 글리프(코드+좌표) 덤프(디버그용).
- **decoded_all.jsonl 재생성**: 전 `docs/problems/**/*.md`를 PDF단위로 `backfill_rosetta.decode_pdf` → `{id,text}` JSONL. ★subject 불일치(아래 함정) 번호폴백 필수.
- **recon.mjs 재빌드**: `cd web && npx esbuild src/lib/reconstruct.ts --bundle --format=esm --platform=node --outfile=/tmp/recon.mjs`.
- **백필 재적용**: `python3 scripts/ingest_kice/backfill_rosetta.py --apply` (기본 dry-run, `--round`으로 한 회차만).

## 남은 일 / 다음 단계
- **6 잔여(0.17%, 사용자에 표시 안 됨)**: 깊은 중첩분수 `\frac{\overline{N}}{…}` ~3, **bbox crop-bleed** ~2(옆 문제 글자가 크롭 경계 침범 — 디코더 아니라 `bbox.py` 영역), 옛 교육과정 1. 전부 렌더 정상, 우선순위 낮음.
- **재구성을 사용자에게 다시 노출하려면 선행**: 도형 라벨 누출 해결(이미지에 픽셀로 박힌 라벨이 재구성에선 밖으로 새 중복/누락). 현재 어드민 전용이라 보류.
- 기타: `docs/TODO.md` 잔여 섹션(랜덤시험 format 자리, 섹션라벨 sliver, 풀이캐시 LLM 병목 등).

## 함정 (gotchas)
- **subject 라벨 불일치** — 옛 가형/나형/단일·모의평가 `.md`의 `subject`(가형) ↔ bbox 추출기 라벨(`공통`) → `decoded.get((subject,num))`가 578개 누락. **번호 폴백**(PDF당 단일과목이면 num으로 유일매칭) 필수. `backfill_rosetta` line~186. **"비-PUA" 아님 — 3564 전부 PUA, 디코드는 됨.**
- **dev 서버 캐시 footgun** — 서버 떠 있을 때 `astro check`/`npm install` → Vite dep 재최적화 stale(504). 콘텐츠 변경 후 `web/.astro`·`web/node_modules/.vite` 클리어 + `server.sh restart` + 사용자 하드리로드.
- **서버 stop 금지** — setsid+watchdog로 Claude와 분리. 명시적 stop만 죽임. `status`로 확인.
- **RTK grep 가로챔** — bash `grep` 결과가 메타문구로 안 보이면 Python으로 파일 검색.
- **디코더 가치 위치** — 사용자용 recon이 아니라 **인제스트 결정론 searchable_text**(LLM 전사 병목 제거). 풀이 캐시(문제 풀기)는 별개로 여전히 LLM.
