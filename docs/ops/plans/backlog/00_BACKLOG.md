---
sources: []
created: 2026-06-28
updated: 2026-06-28
---

# 📝 00_BACKLOG — 장기·미착수 (TODO_LEGACY 이관)

> 분류: Operations / Planning. 착수하면 plan 문서로 승격 → `active/`. 이력 전문: `../reference/TODO_LEGACY_2026-06.md`.

## 필기 캔버스 (사장님 입력·기기테스트 필요)
- [ ] **필기 C 2단계**: 도형 자동스냅→1탭 확정 UI + InteractiveSpec 슬라이더 파라미터 조절(설계 입력 필요). [[project_concept_widgets]]
- [ ] **갈무리→튜터 이미지 피드백**: 채팅 이미지첨부 + 튜터 vision(chat.ts/ChatPanel 개조). 📷내보내기는 됨.
- [ ] **필기 DB 저장**: localStorage → 기기간 동기화(멤버십 백엔드, chat_history 패턴). [[project_membership]]
- [ ] **실펜 테스트 후 버그픽스**: A3 갈무리·도형모드·지우개 커서(헤드리스 미검증) — 아이패드 피드백 후.

## 파이프라인·인프라
- [ ] **★심링크 재발 방지**: 인제스트가 problem-images 심링크를 상대경로로 생성하게(extract_figures 계열). 안 고치면 새 회차 적재 시 절대경로 재발→빌드 재실패.
- [ ] **3D/공간 기출 76개** → Geometry3D 신규(렌더러 설계 결정 필요). [[project_3d_figure_hlr]]
- [ ] **기출 Gemini 교정기 전수**(~5h): 독립검증→쿼터멱등→전수. [[project_gemini_corrector]]
- [ ] **필기 계정 귀속**: 필기 기록 DB화(그래프는 2026-06-29 완료 — graph_history 테이블+/api/graph-history+Graph.tsx 머지동기화). 필기는 데이터 커서 같은 패턴으로 후속. [[project_tutor_chat_ux]] [[project_membership]]

## 선택·보류
- [ ] 완전 캐싱 = Anthropic API 직접 cache_control(현 CLI는 내장 base만). [[project_claude_p_caching]]
- [ ] 검정고시 인제스트(87회차 메인 종료 후). [[project_geomgo_plan]]
- [ ] Gmail MCP 설치(@gongrzhe/server-gmail-autoauth-mcp + Google OAuth, "Gmail 설치해"). — *세션 중 claude.ai Gmail 커넥터 연결됨, 재평가 가능*
- [ ] build_solution_cache usage 로깅(캐싱 절약 직접 측정).

---
## 🔗 지식망 연결
- **상위 분류**: [[00_PLANS]]
