# Math Study Web

LWIP wiki(`../docs/`)를 인터랙티브 대시보드로 보여주는 **Astro 5 + Tailwind v4 + React + react-flow** 정적 사이트.

## 빠른 실행

```bash
# 처음 한 번
npm install

# 개발 서버 (http://localhost:4321)
npm run dev

# 정적 빌드
npm run build
npm run preview
```

`docs/`는 SSOT — web/은 read-only로 빌드 시점에 가져온다. `docs/`를 수정하면 dev server가 즉시 반영.

## 페이지

| 경로 | 설명 |
|:---|:---|
| `/` | 대시보드 — Concept Network 미리보기 + Mastery 도넛 + Due Today + Recent Activity |
| `/graph` | 풀스크린 인터랙티브 DAG (드래그·줌·필터·검색·노드 클릭) |
| `/concepts` `/concepts/[slug]` | 개념 목록 + 상세 (KaTeX, Mermaid, prerequisite 사이드패널) |
| `/problems` `/problems/[slug]` | 문제 목록 + 상세 (한국 시험 출처 메타) |
| `/mistakes` `/mistakes/[slug]` | 오답노트 + D14 gap detection 분석 |
| `/tools` | 학습 자료 |
| `/paths` | D15 학습 경로 (현재 비어 있음) |
| `/log` | docs/log.md 타임라인 |

## 데이터 파이프라인

```
docs/concepts/*.md
    ↓ frontmatter (prerequisites, enables, mastery)
scripts/build-concept-graph.mjs (dagre auto-layout)
    ↓
src/data/concept-graph.json
    ↓
ConceptDAG.tsx (react-flow)
```

`docs/assets/` SVG는 빌드 시 `public/assets/`로 복사된다 (sync-assets.mjs). Markdown 내 상대경로 `../assets/...`는 remark 플러그인이 `/assets/...`로 치환.

## 디자인

- 다크 테마 (Linear/Vercel 풍, zinc-950 기반)
- Mastery 색: rose(unknown) / amber(learning) / emerald(proficient) / sky(mastered)
- 한글 폰트: Pretendard (CDN)
- 수식: KaTeX (rehype-katex)

## 구조

```text
web/
├── astro.config.mjs       # remark/rehype + asset path rewrite
├── src/
│   ├── content.config.ts  # 4 collection Zod 스키마
│   ├── lib/health.ts      # docs/index.md, docs/log.md 파싱
│   ├── layouts/BaseLayout.astro
│   ├── components/
│   │   ├── ConceptDAG.tsx     # ★ react-flow island
│   │   ├── MasteryDonut.tsx   # Chart.js island
│   │   ├── HealthCards.astro / DueTodayList.astro / ActivityFeed.astro
│   │   ├── ConceptCard.astro / Header.astro / Sidebar.astro
│   ├── pages/             # 13 페이지
│   └── styles/global.css  # Tailwind + KaTeX + 디자인 토큰
├── scripts/
│   ├── build-concept-graph.mjs
│   └── sync-assets.mjs
└── public/                # favicon + 자동 동기화된 assets/
```
