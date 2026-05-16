import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const masteryEnum = z.enum(['unknown', 'learning', 'proficient', 'mastered']);
const reviewStateEnum = z.enum(['new', 'learning', 'mature']);

const gradeEnum = z.enum(['중1', '중2', '중3', '고1', '수학1', '수학2', '확률과통계']);

const concepts = defineCollection({
  loader: glob({ pattern: '*.md', base: '../docs/concepts' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    concept_type: z.enum(['unit', 'definition', 'theorem', 'lemma', 'example']),
    grade: gradeEnum.optional(),
    unit: z.string().optional(),
    subunit: z.string().nullable().optional(),
    prerequisites: z.array(z.string()).optional().default([]),
    enables: z.array(z.string()).optional().default([]),
    mastery: masteryEnum,
    mastery_evidence: z.array(z.union([z.string(), z.record(z.unknown())])).optional().default([]),
    mastery_updated: z.coerce.date().optional(),
    review_state: reviewStateEnum.optional(),
    next_review: z.coerce.date().optional(),
    notation_style: z.string().optional(),
  }),
});

const problems = defineCollection({
  loader: glob({ pattern: '*.md', base: '../docs/problems' }),
  schema: z.object({
    sources: z.array(z.string()).optional().default([]),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    source: z.object({
      agency: z.string(),
      exam_type: z.string(),
      year: z.union([z.string(), z.number()]),
      session: z.string().optional(),
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

export const collections = { concepts, problems, mistakes, tools };
