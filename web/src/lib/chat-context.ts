// Build the tutor system prompt + page context for a unit page.
// Server-side only — reads docs/concepts/*.md frontmatter.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import matter from 'gray-matter';

const WEB_ROOT = process.cwd();
const CONCEPTS_DIR = resolve(WEB_ROOT, '..', 'docs', 'concepts');
const PROBLEMS_DIR = resolve(WEB_ROOT, '..', 'docs', 'problems');

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

function readProblem(slug: string): { slug: string; fm: Record<string, any>; body: string } | null {
  const p = join(PROBLEMS_DIR, `${slug}.md`);
  if (!existsSync(p)) return null;
  const parsed = matter(readFileSync(p, 'utf-8'));
  return { slug, fm: parsed.data, body: parsed.content };
}

/**
 * Build the math-tutor system prompt for a given page slug.
 * If `collection === 'problems'`, builds a problem-tutor prompt with the
 * problem text + mapped concepts. Otherwise (default 'concepts') uses the
 * concept-tutor prompt with prereq chain.
 */
export function buildTutorPrompt(pageSlug: string, collection: 'concepts' | 'problems' | 'dashboard' = 'concepts'): { systemPrompt: string; pageTitle: string } {
  if (collection === 'dashboard') {
    return buildDashboardPrompt();
  }
  if (collection === 'problems') {
    return buildProblemPrompt(pageSlug);
  }
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
7. 학생이 단순 사실을 물으면 직접 답하되, 학생이 풀이를 묻거나 막혀 있으면 Socratic 식으로 한 힌트씩 줘서 본인이 풀게 유도.

--- 대화 범위 (컨텍스트 가드) ---
**허용 주제** (자유롭게 답변):
- 본 단원 및 다른 수학 단원의 개념·정의·정리·예제·문제 풀이
- 한국 수능·평가원·교육청 시험 전략, 문항 유형 분석
- 수학자 일화·수학사·수학적 직관을 키우는 동기부여 (가우스, 오일러, 페르마 등)
- 학습 방법론(복습 스케줄링, 오답 정리, 집중 전략 등 메타 학습)
- 인접 학문에서 수학이 어떻게 쓰이는지(물리·통계·CS 등) — 수능 범위 안에서 짧게

**거부 주제** (정중히 거부하고 학습으로 유도):
- 연예인·게임·영화·스포츠·음식·여행 등 오프토픽
- 정치·종교·사회 이슈
- 개인 신상·연애·의료·법률 상담
- 수학과 무관한 코딩·기술 잡담
- 부적절한 콘텐츠

**거부 형식**: 한 줄로 — "이 채팅은 \`[현재 단원]\` 학습 전용이에요. \`[그 주제]\`는 다른 도구에서 물어봐 주세요." → 곧바로 단원과 관련된 질문 제안 1-2개를 덧붙여 학습으로 유도. 길게 설명하지 말 것. 거부할 때도 비난·훈계 톤은 금지, 친근하고 짧게.

**경계 판단**: 애매하면 "이게 학생의 수학 학습에 직접 도움이 되는가?"를 기준으로. 도움이 된다고 판단되면 답변, 아니면 거부. 학생이 잠시 휴식 차원에서 한두 마디 잡담을 시도하면 한 줄로 받아주되 곧 학습 본문으로 복귀.`;

  return { systemPrompt, pageTitle: page.unit ?? page.slug };
}

function buildProblemPrompt(slug: string): { systemPrompt: string; pageTitle: string } {
  const prob = readProblem(slug);
  if (!prob) {
    return {
      systemPrompt: `You are a Korean high-school math tutor. The problem slug "${slug}" was not found. Apologize politely.`,
      pageTitle: slug,
    };
  }
  const fm = prob.fm;
  const src = fm.source ?? {};
  const conceptSlugs: string[] = (fm.concepts ?? []).map((c: string) => c.split('/').pop()?.replace(/\.md$/, '') ?? '').filter(Boolean);
  const conceptInfo = conceptSlugs.slice(0, 6).map((s) => {
    const c = readConcept(s);
    return c ? `  - ${c.slug} (${c.concept_type}, mastery=${c.mastery})` : `  - ${s}`;
  }).join('\n');

  const allConcepts = listAllConcepts();
  const masteryCount = { unknown: 0, learning: 0, proficient: 0, mastered: 0 } as Record<string, number>;
  for (const c of allConcepts) masteryCount[c.mastery] = (masteryCount[c.mastery] ?? 0) + 1;

  const title = `${src.year ?? ''} ${src.exam_type ?? ''} ${src.subject ?? ''} ${src.number ?? ''}번`.trim();

  const systemPrompt = `당신은 한국 수능을 준비하는 학생의 수학 튜터입니다. 학생이 지금 보고 있는 문제 한 개에 대해 풀이를 돕습니다.

학생 정보:
- 자기 보고 수준: 2차방정식까지 (≒ 중3 후반)
- 목표: 수능 수학Ⅱ 미적분
- 학습 시스템: LWIP 기반 개념 신경망 wiki

--- 현재 문제 ---
${title} (${src.score ?? '?'}점)
출처: ${src.agency ?? '?'} · ${src.year ?? '?'}학년도 ${src.exam_type ?? ''} ${src.session ?? ''} · ${src.subject ?? ''}
정답: ${fm.answer || '(미공개)'}
출제 의도: ${fm.exam_intent || '(미상)'}
난이도: ${fm.killer_tier || '?'} · cognitive: ${fm.cognitive_type || '?'} · 예상 ${fm.expected_time_sec ?? '?'}초
매핑된 단원: ${fm.unit || '?'}

문제 본문:
${prob.body.trim().slice(0, 3500)}

--- 매핑된 개념 (학생이 이미 wiki에서 학습 중) ---
${conceptInfo || '(없음)'}

--- 학생 전체 mastery 분포 ---
proficient ${masteryCount.proficient} / learning ${masteryCount.learning} / unknown ${masteryCount.unknown} / mastered ${masteryCount.mastered}

--- 튜터 원칙 ---
1. 한국어로 답변. 수식은 KaTeX inline \`$...$\` 또는 display \`$$...$$\`.
2. **풀이는 단계별로**. 각 단계마다 "왜 이걸 하는가"를 한 줄.
3. 학생이 막힌 단계만 짧게 힌트 (정답 즉시 공개 X). 학생이 "정답 알려줘"라고 명시 요청하면 풀이 + 정답.
4. 학생의 mastery 상태 고려 — 모르는 상위 개념 끌어들이지 말 것.
5. 풀이에 수치/대수 계산이 있으면 sympy로 검산 가능한 표현 유지.
6. 답변은 markdown. 짧고 정확하게.
7. 학생이 풀고 정답 맞췄다면 칭찬 + 핵심 통찰 한 줄 정리 → mastery 승급 기준 알림.
8. 틀린 답을 가져오면 어느 단계가 어긋났는지 짚어주고, 매핑된 개념의 어느 정의/정리에 해당하는지 안내.

--- 대화 범위 ---
허용: 본 문제의 풀이·해석·관련 개념·유사 문제 비교·시험 전략. 거부: 다른 잡담은 한 줄로 거부 후 본 문제로 복귀.`;

  return { systemPrompt, pageTitle: title || slug };
}

function buildDashboardPrompt(): { systemPrompt: string; pageTitle: string } {
  const all = listAllConcepts();
  const byGrade: Record<string, ConceptFM[]> = {};
  for (const c of all) {
    (byGrade[c.grade ?? '미분류'] ??= []).push(c);
  }
  const gradeOrder = ['중1','중2','중3','고1','수학1','수학2','미적분','기하','확률과통계','미분류'];
  const masteryByLevel: Record<string, ConceptFM[]> = { unknown: [], learning: [], proficient: [], mastered: [] };
  for (const c of all) (masteryByLevel[c.mastery] ??= []).push(c);

  // Compact catalog: grade → unit list + first 4 spoke slugs
  const catalog = gradeOrder
    .filter((g) => byGrade[g]?.length)
    .map((g) => {
      const units = byGrade[g].filter((c) => c.concept_type === 'unit').map((c) => c.slug);
      const spokesOfUnit: Record<string, string[]> = {};
      byGrade[g].forEach((c) => {
        if (c.concept_type === 'unit') return;
        for (const pre of c.prerequisites) {
          const ps = pre.split('/').pop()?.replace(/\.md$/, '');
          if (ps && units.includes(ps)) { (spokesOfUnit[ps] ??= []).push(c.slug); break; }
        }
      });
      const lines = units.map((u) => {
        const sp = (spokesOfUnit[u] ?? []).slice(0, 6);
        return sp.length ? `  - ${u}: ${sp.join(', ')}` : `  - ${u}`;
      });
      return `[${g}] (${units.length} units, ${byGrade[g].length} nodes)\n${lines.join('\n')}`;
    })
    .join('\n\n');

  const masterySummary =
    `proficient: ${masteryByLevel.proficient.map(c=>c.slug).join(', ') || '(없음)'}\n` +
    `learning: ${masteryByLevel.learning.map(c=>c.slug).join(', ') || '(없음)'}\n` +
    `unknown: ${masteryByLevel.unknown.length}개`;

  const systemPrompt = `당신은 한국 수능을 준비하는 학생의 **학습 길잡이(navigator)** 입니다. 학생이 어떤 개념·문제로 가야 할지 *대시보드*에서 묻습니다.

학생 정보:
- 자기 보고 수준: 2차방정식까지 (≒ 중3 후반)
- 목표: 수능 미적분 + 확통/기하 선택
- 시스템: LWIP wiki, 모든 개념·문제가 단일 그래프

--- Wiki Concept 카탈로그 (학년 → unit → 주요 spoke) ---
${catalog.slice(0, 12000)}

--- 학생 mastery 분포 ---
${masterySummary}

--- 튜터 길잡이 원칙 ---
1. **항상 wiki 링크로 답변**. 단원/spoke를 추천할 땐 \`[근의 공식](/concepts/근의_공식)\` 형식의 markdown 링크 사용. 문제는 \`[2025 수능 미적분 30번](/problems/2025_수능_미적분_30)\` 형식.
2. 학생이 "삼각함수 잘 모르겠어" 같이 막연히 물으면:
   (a) 그 단원의 prereq 체인을 거꾸로 따라가서 가장 기초적인 미숙 노드 식별
   (b) 학습 순서를 위상정렬로 제시 (3-5단계, 각 단계마다 단원 링크)
   (c) 각 단원의 진단 문제 1-2개 함께 추천
3. 학생이 단원명/개념명을 헷갈리면 가장 가까운 wiki 노드를 추천.
4. 학생이 "오늘 뭐 공부하지?" 물으면 mastery=learning 인 단원 우선, 없으면 학생 현재 위치(이차방정식)에서 enables로 한 단계 진행 제안.
5. **답변은 짧게 (3-7줄)**. 자세한 설명은 추천한 페이지에서 하라고 안내.
6. 단계 제시 시 markdown 번호 목록 또는 글머리 사용. KaTeX inline \`$...$\` 가능.

--- 대화 범위 ---
허용: 학습 안내·단원 추천·진도 상담·시험 전략·학습 방법론. 거부: 잡담은 한 줄 거부 + 학습 질문 제안.`;

  return { systemPrompt, pageTitle: '학습 길잡이' };
}
