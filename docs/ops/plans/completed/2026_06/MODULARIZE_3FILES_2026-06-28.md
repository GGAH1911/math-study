---
created: 2026-06-28
updated: 2026-06-28
status: DONE
priority: P2
owner: "@insung + 튜터"
---

# 1·2·3순위 모듈화 (chat-context · ConceptDAG · build_solution_cache)

> [[feedback_module_first]] 원칙 적용. ChatPanel(1972→582) 이후 후속 3파일. 회귀방지=베이스라인→순수이동
> →타입체커(py는 import+unit)→스모크→체크포인트 커밋.

## ① chat-context.ts 1096 → 488줄 (−55%) ✅
- `lib/prompts/tutor-rules.ts` — MATH_TYPOGRAPHY_RULE·GRAPHICS_GUIDE(415줄)·FOLLOWUP_VERIFICATION_RULE(정적 문자열).
- `lib/concept-fs.ts` — slugOf·safeJoin·readConcept·walkMdSync·listAllConcepts·_bigrams·searchConcepts·readProblem + ConceptFM·dir.
- 본체=빌더만. searchConcepts 재export로 chat.ts 무영향. astro check 0·컴파일 200.

## ② ConceptDAG.tsx 1238 → 1056줄 ✅
- `lib/dag-types.ts`(GraphNode/Edge/Data/ColorMode) · `lib/dag-layout.ts`(dagreLayout 순수) ·
  `components/ConceptNode.tsx`(노드 렌더). viz 본체(Inner 980줄)는 단일책임이라 유지.
- astro check 0·컴파일 200·**graph 페이지 렌더 200(149 마운트)**.

## ③ build_solution_cache.py 991 → 877줄 ✅
- `scripts/solve_prompts.py` — build_prompt·build_text_prompt·build_openbook_prompt·build_promote_prompt(자족적).
- 검증: py_compile·import build_solution_cache(모듈레벨 참조 OK)·unit 호출(4빌더 문자열 반환).
- ※검증/게이트 클러스터(run_verifier·hardcode_gate·param_mutation_gate 등)는 결합 높고 **풀파이프라인
  변이테스트 검증 필요** → 보수적으로 빌더만. 추후 솔버 작업 시 곁들이기.

## 결과
3파일 합 3325 → 2421줄(본체), 신규 모듈 6개. 렌더러 본체·viz core·검증게이트는 의도적 유지(단일책임/검증비용).
