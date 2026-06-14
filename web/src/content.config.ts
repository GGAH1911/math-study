import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const masteryEnum = z.enum(['unknown', 'learning', 'proficient', 'mastered']);
const reviewStateEnum = z.enum(['new', 'learning', 'mature']);

const gradeEnum = z.enum(['중1', '중2', '중3', '고1', '수학1', '수학2', '미적분', '기하', '확률과통계']);
const domainEnum = z.enum(['수와식', '방정식', '함수', '도형', '확률통계', '논리']);

const concepts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../docs/concepts' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    concept_type: z.enum(['unit', 'definition', 'theorem', 'lemma', 'example']),
    grade: gradeEnum.optional(),
    domain: domainEnum.optional(),
    unit: z.string().optional(),
    subunit: z.string().nullable().optional(),
    prerequisites: z.array(z.string()).optional().default([]),
    enables: z.array(z.string()).optional().default([]),
    mastery: masteryEnum,
    mastery_evidence: z.array(z.union([z.string(), z.record(z.string(), z.unknown())])).optional().default([]),
    mastery_updated: z.coerce.date().optional(),
    review_state: reviewStateEnum.optional(),
    next_review: z.coerce.date().optional(),
    notation_style: z.string().optional(),
  }),
});

const problems = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../docs/problems' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    source: z.object({
      agency: z.string(),
      exam_type: z.string(),
      year: z.union([z.string(), z.number()]),
      session: z.string().optional(),
      grade: z.string().optional(),
      subject: z.string(),
      number: z.union([z.string(), z.number()]),
      score: z.union([z.string(), z.number()]).optional(),
    }).optional(),
    problem_id: z.union([z.string(), z.number(), z.null()]).optional(),
    concepts: z.array(z.string()).optional().default([]),
    status: z.enum(['unsolved', 'solved', 'review']),
    difficulty: z.string().optional(),
    last_attempted: z.coerce.date().optional(),
    review_state: reviewStateEnum.optional(),
    next_review: z.coerce.date().optional(),
    figure_engine: z.string().optional(),
    // Tier 1 extended (Stage 1 KICE ingest)
    format: z.enum(['choice', 'numeric', 'descriptive']).optional(),
    has_image: z.boolean().optional(),
    image_paths: z.array(z.string()).optional().default([]),
    answer: z.string().nullable().optional(),
    official_pass_rate: z.number().nullable().optional(),
    official_solution_url: z.string().nullable().optional(),
    // Tier 2 (LLM-mapped)
    unit: z.string().nullable().optional(),
    exam_intent: z.string().optional(),
    killer_tier: z.enum(['early', 'mid', 'high', 'killer']).nullable().optional(),
    cognitive_type: z.enum(['계산', '개념', '응용', '추론', '통합']).nullable().optional(),
    expected_time_sec: z.number().nullable().optional(),
    // v2 (PNG-First) — body is a single PNG crop; searchable_text is the
    // vision-extracted plain-text shadow used by the tutor LLM and search.
    problem_image: z.string().optional(),
    has_figure: z.boolean().optional(),
    figure_image: z.string().optional(),  // 추출·stitch 한 도형만 잘라낸 PNG (재구성 뷰용)
    figure_after_line: z.number().optional(),  // 재구성 본문 몇 번째 줄 뒤에 도형 삽입 (백필이 PDF 위치로 계산)
    searchable_text: z.string().optional(),
    // Stage C — vision LLM이 ingest 시 추출한 도형 spec (geometry/plot/numberline/chart).
    // 채워져 있으면 problem 페이지가 raw PNG 외에 spec 기반 SVG 도 함께 렌더 가능.
    // 모든 수능 도형이 이 spec으로 표현 가능한 건 아님 — fallback은 PNG.
    figure_spec: z.object({
      kind: z.enum(['geometry', 'plot', 'numberline', 'chart']),
      spec: z.record(z.string(), z.unknown()),
      confidence: z.number().min(0).max(1).optional(),
    }).optional(),
    // 검증된 풀이 캐시 (scripts/build_solution_cache.py 생성). 튜터 레퍼런스 + 페이지 "풀이 보기".
    solution: z.object({
      answer_value: z.string().optional(),
      verified: z.boolean().optional(),
      generated_by: z.string().optional(),         // 검증기까지 통과한 최종 모델(캐시된 풀이)
      solved_by: z.string().optional(),            // 최초로 답 맞힌 모델 = 난이도 신호(검증기 통과와 무관)
      source: z.string().optional(),               // 'text'=searchable_text만으로 검증 통과 → 튜터가 텍스트 신뢰 가능
      text_ok: z.boolean().optional(),             // 재라벨: text-Haiku가 텍스트만으로 정답 재현(기존 풀이는 보존, 텍스트 신뢰+난이도=haiku)
      escalation: z.array(z.object({               // 그 전 모델 탈락 사유(verify-fail=검증기 탓 / ans-wrong=오답)
        model: z.string(), reason: z.string(),
      })).optional(),
      verifier: z.string().optional(),
      steps: z.array(z.string()).optional().default([]),
    }).optional(),
  }),
});

const mistakes = defineCollection({
  loader: glob({ pattern: '*.md', base: '../docs/mistakes' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    problem: z.string().optional(),
    error_type: z.enum(['concept_gap', 'careless', 'wrong_approach', 'unknown_method']),
    lesson: z.string().optional(),
    revisit_date: z.coerce.date().optional(),
    review_state: reviewStateEnum.optional(),
    next_review: z.coerce.date().optional(),
  }),
});

const tools = defineCollection({
  loader: glob({ pattern: '*.md', base: '../docs/tools' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    kind: z.enum(['book', 'lecture', 'workbook', 'site', 'other']).optional(),
    title: z.string().optional(),
    url: z.string().optional(),
  }),
});

const syntheses = defineCollection({
  loader: glob({ pattern: '*.md', base: '../docs/syntheses' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    // 출처 concept (promote 시점의 원본 페이지). 보통 `docs/concepts/<slug>.md` 형식.
    origin_concept: z.string().optional(),
    // 어디서 끌어왔는지 — 현재는 채팅 promote 만 (`chat`).
    promoted_from: z.string().optional(),
    review_state: reviewStateEnum.optional(),
    next_review: z.coerce.date().optional(),
  }),
});

export const collections = { concepts, problems, mistakes, tools, syntheses };
