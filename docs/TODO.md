# TODO — 솔버/파이프라인 백로그

> 갱신: 2026-06-07 · 튜터 그래프 정확도(plot 교점·geometry 방향) + 크롭/게이트 4개 백엔드 균일화 후 잔여.

## 완료 (2026-06-06)
- [x] 백필 blind→open-book + 하드코딩 게이트(변이테스트) + 인제스트 본류 반영
- [x] 단답형 additive 솔버 + lite→full 승격(파라미터 변이 게이트)
- [x] KEEP-GOLD 51개 → **100% 솔버화** (회복백필 43 + 승격 29 + 수동 8)
- [x] 텍스트 품질 게이트(글리프 자동 재전사) + agent.md D17(타일 규칙)
- [x] 무결성 가드(audit_solvers) + 일관성 게이트(consistency_gate: format·답 오분류) + post_ingest_sync 자동화
- [x] regen_one 에러출력 검증 / 객관식 CANDIDATE↔gold 매핑 강제
- [x] 게이트가 찾은 추가 결함 수정: 2022·2023 기하 23/24, 단일_06/18 (format 오분류)

## 완료 (2026-06-07)
- [x] **튜터 그래프 점 정확도** — plot 교점/근을 LLM 손계산 대신 렌더러 이분법 계산(Graph.tsx `intersections`/`roots` + bisectRoot), geometry 자기닮음 방향 게이트(sympy.ts `assert_segments_disjoint`/`_cross`, chat-context 규칙), plot JSON sanitize 강화(LaTeX 백슬래시 보존·배열 수식 평가)
- [x] **상단 크롭 보정** — `crop_problem`(원래경계+headroom 18px, 스캔 제거) 전 3056문제 적용 + 인제스트 4개 백엔드 반영(**gyo3 누락분 포함**) + recrop_v3 footgun 제거 → `crop_by_gap` 호출자 0(은퇴)
- [x] **백엔드 게이트 균일화** — text_quality_gate(v2·gyo3 누락분)·consistency_gate 캐시前 인라인·풀이캐시 체이닝(gyo3 누락분) 추가 → 4개 백엔드(v2/ganah/gyo12/gyo3) 동일 템플릿

## 잔여 (난이도순)
- [ ] **크로스-스크립트 게이트/타일 일관성 감사** — 이번엔 *인제스트 4개 백엔드*만 균일화. 풀이캐시(build_solution_cache)·백필(backfill_solvers)·vision 폴백(vision_meta)·promote 가 동일 게이트/타일(D17) 규약 쓰는지 전수 대조 남음.
- [ ] **synthesis 페이지 그래프 렌더** — `docs/syntheses/` 의 promote된 plot/geometry 펜스가 Astro `<Content />`(plot 변환 플러그인 없음)에서 코드블록으로만 표시됨. remark 플러그인으로 실제 그래프 렌더 필요(튜터 런타임과 별개 경로).
- [ ] **PUA-silent 손상 감지** — text_meta 인제스트 시점에 PDF 텍스트레이어 PUA 디코드 이상 → 타일-vision 전사 승급. (silent라 감지 자체가 난제; 현 게이트는 loud 손상만)
- [ ] **신규 인제스트 full 솔버에 파라미터 변이 게이트** — 현재 backfill/promote만. build_one 객관식 수용에도 solve(**계수) 규약+param 게이트 적용.
- [ ] **brute-force 프롬프트 모드** — 조합/경우의수 단원 자동화(현재 수동 검증만).
- [ ] searchable_text 생성에 타일 적용(D17) — 속도 영향 검토 후.
