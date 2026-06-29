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
- [x] **필기 DB 저장** (2026-06-29 완료): handwriting 테이블 + /api/handwriting + InkCanvas 디바운스 push·로컬우선 hydration. [[project_membership]]
- [ ] **실펜 테스트 후 버그픽스**: A3 갈무리·도형모드·지우개 커서(헤드리스 미검증) — 아이패드 피드백 후.

## 파이프라인·인프라
- [x] **심링크 재발 방지** (완료확인 2026-06-29): _ensure_web_symlink 가 이미 os.path.relpath 로 상대경로 심링크 생성(절대경로 심링크 0개 확인). extract_figures 는 심링크 미생성. backlog 항목 stale였음.
- [ ] **3D/공간 기출 76개** → Geometry3D 신규(렌더러 설계 결정 필요). [[project_3d_figure_hlr]]
- [ ] **기출 Gemini 교정기 전수**(~5h): 독립검증→쿼터멱등→전수. [[project_gemini_corrector]]
- [x] **그래프·필기 계정 귀속** (2026-06-29 완료): graph_history·handwriting 테이블 양쪽 DB동기화. 비로그인=localStorage 폴백. [[project_tutor_chat_ux]] [[project_membership]]

## 선택·보류
- [ ] 완전 캐싱 = Anthropic API 직접 cache_control(현 CLI는 내장 base만). [[project_claude_p_caching]]
- [ ] 검정고시 인제스트(87회차 메인 종료 후). [[project_geomgo_plan]]
- [ ] Gmail MCP 설치(@gongrzhe/server-gmail-autoauth-mcp + Google OAuth, "Gmail 설치해"). — *세션 중 claude.ai Gmail 커넥터 연결됨, 재평가 가능*
- [ ] build_solution_cache usage 로깅(캐싱 절약 직접 측정).

---
## 🔗 지식망 연결
- **상위 분류**: [[00_PLANS]]
