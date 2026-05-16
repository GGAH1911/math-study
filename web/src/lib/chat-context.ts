// Build the tutor system prompt + page context for a unit page.
// Server-side only — reads docs/concepts/*.md frontmatter.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import matter from 'gray-matter';

const WEB_ROOT = process.cwd();
const CONCEPTS_DIR = resolve(WEB_ROOT, '..', 'docs', 'concepts');

type ConceptFM = {
  slug: string;
  concept_type: string;
  grade?: string;
  unit?: string;
  prerequisites: string[];
  enables: string[];
  mastery: string;
  body: string;
};

function slugOf(p: string) {
  return p.split('/').pop()?.replace(/\.md$/, '') ?? p;
}

function readConcept(slug: string): ConceptFM | null {
  const p = join(CONCEPTS_DIR, `${slug}.md`);
  if (!existsSync(p)) return null;
  const raw = readFileSync(p, 'utf-8');
  const parsed = matter(raw);
  const fm = parsed.data;
  return {
    slug,
    concept_type: fm.concept_type ?? 'definition',
    grade: fm.grade,
    unit: fm.unit,
    prerequisites: (fm.prerequisites ?? []).map((p: string) => slugOf(p)),
    enables: (fm.enables ?? []).map((p: string) => slugOf(p)),
    mastery: fm.mastery ?? 'unknown',
    body: parsed.content,
  };
}

function listAllConcepts(): ConceptFM[] {
  if (!existsSync(CONCEPTS_DIR)) return [];
  return readdirSync(CONCEPTS_DIR)
    .filter((f) => f.endsWith('.md'))
    .map((f) => readConcept(f.replace(/\.md$/, '')))
    .filter((c): c is ConceptFM => c !== null);
}

/**
 * Build the math-tutor system prompt for a given page slug.
 * Includes:
 *  - the page's own markdown body (학습 목표 + 다룰 정의/정리/예제)
 *  - each direct prerequisite's body excerpt (학습 목표만)
 *  - the student's mastery overview across the whole graph
 *  - LWIP Chapter 7 governance summary (so the tutor follows house rules)
 */
export function buildTutorPrompt(pageSlug: string): { systemPrompt: string; pageTitle: string } {
  const page = readConcept(pageSlug);
  if (!page) {
    return {
      systemPrompt: `You are a Korean high-school math tutor. The page slug "${pageSlug}" was not found. Apologize politely and ask the user to choose another page.`,
      pageTitle: pageSlug,
    };
  }
  const allConcepts = listAllConcepts();
  const masteryByLevel: Record<string, string[]> = {
    unknown: [], learning: [], proficient: [], mastered: [],
  };
  for (const c of allConcepts) {
    (masteryByLevel[c.mastery] ??= []).push(`${c.slug}${c.grade ? `(${c.grade})` : ''}`);
  }

  const extractObjectives = (body: string): string => {
    const m = body.match(/##\s+학습\s*목표\s*\n([\s\S]+?)(\n##|\n$)/);
    if (!m) return '';
    return m[1].trim().split('\n').map((l) => l.replace(/^-\s*/, '• ')).join(' ').slice(0, 200);
  };

  const prereqInfo = page.prerequisites
    .map((p) => readConcept(p))
    .filter((c): c is ConceptFM => !!c)
    .map((c) => `  - ${c.slug}${c.grade ? ` (${c.grade})` : ''} [${c.mastery}]: ${extractObjectives(c.body)}`)
    .join('\n');

  const enablesInfo = page.enables
    .map((p) => readConcept(p))
    .filter((c): c is ConceptFM => !!c)
    .map((c) => `  - ${c.slug}${c.grade ? ` (${c.grade})` : ''}`)
    .join('\n');

  const systemPrompt = `당신은 한국 수능을 준비하는 학생의 수학 튜터입니다.

학생 정보:
- 자기 보고 수준: 2차방정식까지 (≒ 중3 후반)
- 목표: 수능 수학Ⅱ 미적분
- 학습 시스템: LWIP 기반 개념 신경망 wiki

--- 현재 페이지 ---
단원: ${page.unit ?? page.slug}  (학년: ${page.grade ?? '미지정'}, type: ${page.concept_type})
Mastery: ${page.mastery}

본문 (학생이 보고 있는 페이지):
${page.body.trim().slice(0, 2000)}

--- 직접 선수 개념 (prerequisites) ---
${prereqInfo || '(없음 — 기초 노드)'}

--- 이 개념이 가능케 하는 것 (enables) ---
${enablesInfo || '(아직 정의 안 됨)'}

--- 학생의 전체 mastery 분포 ---
- proficient (잘 앎): ${masteryByLevel.proficient.length}개 — ${masteryByLevel.proficient.join(', ') || '(없음)'}
- learning (학습 중): ${masteryByLevel.learning.length}개 — ${masteryByLevel.learning.join(', ') || '(없음)'}
- unknown (아직): ${masteryByLevel.unknown.length}개

--- 튜터 원칙 (LWIP Chapter 7) ---
1. 한국어로 답변. 수식은 KaTeX inline \`$...$\` 또는 display \`$$...$$\` 사용.
2. 한국 고등학교 교육과정 용어를 우선 (근의 공식, 도함수, 정적분 등).
3. 학생의 mastery 상태를 고려해 답변. 학생이 아직 모르는 상위 개념을 끌어들이지 말고, 이미 아는(proficient) 개념에 기반해 설명.
4. 수치/대수 계산이 포함되면 단계를 명확히 보이고, 학생이 sympy 검산을 직접 할 수 있도록 식을 명시.
5. 답변은 markdown으로 작성. 코드 블록은 \`\`\`python 식으로 명시.
6. 짧고 정확하게. 모호한 답변 금지. 학생이 stuck한 단계를 정확히 짚어 한 단계 진전시키는 것이 목표.
7. 학생이 단순 사실을 물으면 직접 답하되, 학생이 풀이를 묻거나 막혀 있으면 Socratic 식으로 한 힌트씩 줘서 본인이 풀게 유도.`;

  return { systemPrompt, pageTitle: page.unit ?? page.slug };
}
