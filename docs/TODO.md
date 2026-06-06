# TODO — 솔버/파이프라인 백로그

> 갱신: 2026-06-06 · open-book 솔버 파이프라인 + 게이트 + KEEP-GOLD 100% 회복 후 잔여.

## 완료 (2026-06-06)
- [x] 백필 blind→open-book + 하드코딩 게이트(변이테스트) + 인제스트 본류 반영
- [x] 단답형 additive 솔버 + lite→full 승격(파라미터 변이 게이트)
- [x] KEEP-GOLD 51개 → **100% 솔버화** (회복백필 43 + 승격 29 + 수동 8)
- [x] 텍스트 품질 게이트(글리프 자동 재전사) + agent.md D17(타일 규칙)
- [x] 무결성 가드(audit_solvers) + 일관성 게이트(consistency_gate: format·답 오분류) + post_ingest_sync 자동화
- [x] regen_one 에러출력 검증 / 객관식 CANDIDATE↔gold 매핑 강제
- [x] 게이트가 찾은 추가 결함 수정: 2022·2023 기하 23/24, 단일_06/18 (format 오분류)

## 잔여 (난이도순)
- [ ] **PUA-silent 손상 감지** — text_meta 인제스트 시점에 PDF 텍스트레이어 PUA 디코드 이상 → 타일-vision 전사 승급. (silent라 감지 자체가 난제; 현 게이트는 loud 손상만)
- [ ] **신규 인제스트 full 솔버에 파라미터 변이 게이트** — 현재 backfill/promote만. build_one 객관식 수용에도 solve(**계수) 규약+param 게이트 적용.
- [ ] **brute-force 프롬프트 모드** — 조합/경우의수 단원 자동화(현재 수동 검증만).
- [ ] **상단 크롭 보정** — 일부 문제 이미지 상단(첫 줄 위첨자) 잘림. 사용자용 이미지 deterministic 재크롭.
- [ ] searchable_text 생성에 타일 적용(D17) — 속도 영향 검토 후.
