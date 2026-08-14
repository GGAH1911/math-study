// Build the tutor system prompt + page context for a unit page.
// Server-side only — reads docs/concepts/*.md frontmatter.
import { readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { tutorWidgetMeta } from './concept-widgets-server';
import { misconceptionsBlock } from './concept-misconceptions-server';
import { MATH_TYPOGRAPHY_RULE, GRAPHICS_GUIDE, FOLLOWUP_VERIFICATION_RULE } from './prompts/tutor-rules';
import { figure3DBlock } from './figures-3d';
import { type ConceptFM, WEB_ROOT, slugOf, readConcept, listAllConcepts, readProblem } from './concept-fs';
export { searchConcepts } from './concept-fs';   // 노드별 위젯 메타(bespoke+spec, 튜터 인지용)


/**
 * Build the math-tutor system prompt for a given page slug.
 * If `collection === 'problems'`, builds a problem-tutor prompt with the
 * problem text + mapped concepts. Otherwise (default 'concepts') uses the
 * concept-tutor prompt with prereq chain.
 */
// 작은 모델 (gemma4 e4b/e2b, 7b 이하) 용 압축 prompt — 1-2KB.
// 우리 full prompt (8KB+) 의 가이드를 작은 모델이 다 못 따르니 핵심 룰 + few-shot 만.
// 직접 요청 ("그려봐", "보여줘") 시 sympy 단계 건너뛰고 즉시 graphic block emit 강조.
export function buildCompactTutorPrompt(pageSlug: string, collection: 'concepts' | 'problems' | 'dashboard' = 'concepts'): { systemPrompt: string; pageTitle: string; allowedDirs?: string[]; imagePaths?: string[] } {
  const full = buildTutorPrompt(pageSlug, collection);
  if (full.systemPrompt.includes('was not found')) return full; // ★진짜 못 찾음만 fallback (pageTitle===slug 오판 방지: unit 없는 개념도 compact 사용)

  // 페이지 컨텍스트 추출 (간략)
  const fullText = full.systemPrompt;
  const pageContext = fullText.match(/--- 현재 (?:페이지|문제)[\s\S]*?(?=\n##|\n---|\n\*\*|$)/)?.[0]?.slice(0, 1500) ?? '';
  // 이미지가 있는 problem 은 본문 text 일부러 안 넣음 — 학생 메시지에 첨부된 이미지로만 풀어야 함.
  // 이미지 없는 problem (또는 concept/dashboard) 만 문제 본문 인용.
  const hasImage = /문제 이미지 \(유일한 원본 소스\)/.test(fullText);
  const problemText = hasImage
    ? ''
    : fullText.match(/문제 본문:\s*\n([\s\S]+?)(?=\n---|$)/)?.[1]?.slice(0, 800) ?? '';

  const widget = collection === 'concepts' ? tutorWidgetMeta(pageSlug) : null;

  const compact = `당신은 한국 고등학교 수학 튜터입니다. 학생이 "${full.pageTitle}" 페이지에 있습니다.

${pageContext ? `## 페이지 컨텍스트\n${pageContext}\n` : ''}
${widget ? `## 이 페이지의 인터랙티브 위젯 (적극 활용)\n본문 위에 **${widget.label}** 위젯이 이미 있습니다. ${widget.tutorHint}\n학생이 시각적 이해가 필요하거나 막힐 때, (이 튜터는 도형을 직접 못 그리니) 큰 모델 권유 대신 **"위 위젯에서 ___ 해보세요"** 라고 그 위젯을 직접 조작하도록 구체적으로 안내하고, 무엇을 보게 될지 짚어 주세요.\n` : ''}
${problemText ? `## 문제\n${problemText}\n` : ''}
${hasImage ? `## 문제 이미지 (유일한 원본)
이 문제의 본문·식·도형은 첨부된 이미지로만 확인. OCR 텍스트는 부정확해 의도적으로 제외했음.
첫 응답 전에 이미지를 먼저 본 뒤 풀이 시작. 못 보거나 vision 미지원이면 거부 후 큰 모델 권유.
` : ''}

## 응답 규칙 (반드시 준수)

1. **간결하게** — 한국어 존댓말, 짧은 문장. 불필요한 친절·반복·서론 금지.

2. **모든 수식은 KaTeX**: 인라인 \`$x^2$\`, 디스플레이 \`$$\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1$$\`. ASCII \`x^2/a^2\` 절대 금지.

3. **소크라테스 방식** — 정답은 학생이 직접 찾도록. 답 자체를 알려주지 말고 한 단계 힌트만.

4. **그래픽·도형 emit 금지** — 이 모델은 도형/그래프 생성을 지원하지 않습니다.
   학생이 "그려봐", "도형 보여줘", "그래프 보여줘" 같이 요청하면 한 줄로 답:
   > "이 모델은 도형 생성을 지원하지 않아요. 우측 상단 ⚙ BYOK 설정에서 \`anthropic/claude-haiku-4.5\` 같은 큰 모델로 바꾸시면 도형을 그릴 수 있어요."
   그리고 도형 *대신* 좌표·관계를 텍스트로 설명. \`\`\`geometry\`\`\`, \`\`\`geometry3d\`\`\`, \`\`\`plot\`\`\`,
   \`\`\`interactive\`\`\`, \`\`\`svg\`\`\` 같은 fenced block 절대 emit 금지.

## 금기

- 답 자체 노출 (1번부터 5번 보기 중 골라주기 등) 금지
- "sympy/python/코드 실행/백엔드" 같은 기술 용어 학생에게 노출 금지
- 학습 무관 주제 (정치·연예 등) — 한 줄로 거부 + 학습으로 복귀
- 그래픽 fenced block (\`\`\`geometry\`\`\`, \`\`\`geometry3d\`\`\`, \`\`\`plot\`\`\` 등) 사용 금지
`;

  return { systemPrompt: compact, pageTitle: full.pageTitle, allowedDirs: full.allowedDirs, imagePaths: full.imagePaths };
}

export function buildTutorPrompt(pageSlug: string, collection: 'concepts' | 'problems' | 'dashboard' = 'concepts', userMastery?: string, opts?: { misconceptions?: boolean }): { systemPrompt: string; pageTitle: string; allowedDirs?: string[]; imagePaths?: string[] } {
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
  // 이 학생의 현재 mastery(promote 판정 기준). 없으면 frontmatter 폴백
  // (frontmatter mastery 는 전역이라 멤버십 후 사용자 실제 상태가 아님 — chat.ts 가 주입).
  const currentMastery = userMastery ?? page.mastery;
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

  const widget = collection === 'concepts' ? tutorWidgetMeta(pageSlug) : null;

  const systemPrompt = `당신은 한국 수능을 준비하는 학생의 수학 튜터입니다.

학생의 현재 수준은 **특정 학년·수준으로 고정 가정하지 말 것** — 대화 맥락과 (제공되면)
아래 mastery 분포에서 파악한다. 모르면 한 단계 물어 확인.
학습 시스템: LWIP 기반 개념 신경망 wiki (수능 수학 대비).

--- 현재 페이지 ---
단원: ${page.unit ?? page.slug}  (학년: ${page.grade ?? '미지정'}, type: ${page.concept_type})
Mastery: ${currentMastery}${userMastery ? ' (이 학생의 실제 현재 상태)' : ''}

본문 (학생이 보고 있는 페이지):
${page.body.trim().slice(0, 2000)}
${widget ? `
--- 이 페이지의 인터랙티브 위젯 (그래픽 그리기보다 우선 활용) ---
본문에 이 개념의 인터랙티브 위젯(**${widget.label}**)이 있습니다. ${widget.tutorHint}
직접 그래픽을 그리기 전에 먼저 그 위젯을 직접 조작하도록 안내하는 것이 핵심입니다 — 학생이 직접 만지며 이해하는 게 더 효과적입니다.
` : ''}${opts?.misconceptions === true ? misconceptionsBlock(pageSlug) : ''}
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
3. 학생의 mastery 상태를 고려. 학생이 아직 모르는 상위 개념을 끌어들이지 말고, 이미 아는(proficient) 개념에 기반해 설명.
4. 답변은 markdown. 수치/대수 계산은 정확한 식 형태 유지.
5. 짧고 정확하게. 학생이 막힌 단계를 정확히 짚어 한 걸음만 진전시키는 것이 목표.

--- Mastery 승급/강등 판정 (agent.md D13) ---
이 단원에서 이 학생의 **현재 상태는 \`${currentMastery}\`** 다. promote 의 \`to\` 는 반드시
이 현재 상태를 기준으로 정한다 — 절대 레벨을 그냥 던지지 말 것.

레벨 순서: unknown < learning < proficient < mastered.

**핵심 규칙 (반드시):**
- \`to\` 는 **현재 상태보다 한 단계 높을 때만**(=승급). 현재(\`${currentMastery}\`)가 이미 그
  단계 이상이면 promote 를 **emit하지 말 것**. 학생이 기본 문제를 잘 풀어도, 현재가 이미
  proficient 면 그대로 두거나(emit X) mastered 만 제안한다.
- ⚠️ 현재(\`${currentMastery}\`)보다 **낮은** \`to\` 는 **강등**이다. "정의·예제를 잘 풀었다"는
  강등 사유가 절대 아니다 — 잘 푼 건 현 상태 유지 또는 승급의 근거다. 잘 했는데 낮은 to 를
  쓰면 학생 데이터를 깎는 버그가 된다.
- 강등(낮은 to)은 학생이 **이전에 알던 것을 지금 명백히 틀려** 현 단계 자격이 없음이 드러난
  명확한 퇴행일 때만, 그 퇴행 증거를 reason 에 구체적으로 적는다.
- 판단은 보수적으로. 애매하면 emit하지 말 것.

승급 기준 (현재가 그 직전 단계일 때만 해당 to 를 쓴다):
- unknown → learning: 정의·기본 예제 1회 무리 없이 통과
- learning → proficient: 4점 수준 문항 2회 무오답 통과
- proficient → mastered: 킬러 문항(20·21·22·28·29·30번대) 1회 통과

emit 형식 (반드시 JSON, evidence는 선택):
\`\`\`promote
{"to": "learning", "reason": "이차방정식 인수분해 5문제 연속 정답", "evidence": ["docs/problems/2025_수능_미적분_15.md"]}
\`\`\`

이걸 emit하면 사용자에게 승급 확인 카드가 표시된다. **확실하지 않으면 emit하지 말 것** — 매 응답마다 emit X. 학생의 성취가 분명할 때만.

${MATH_TYPOGRAPHY_RULE}
${GRAPHICS_GUIDE}
- 인라인 LaTeX(\`$...$\`)로도 충분히 설명 가능하면 그래프 안 써도 OK.

--- 답을 직접 알려주지 말 것 (핵심 hard rule) ---
**다음 행동은 절대 금지**:
- 학생이 예제·문제·계산에서 틀린 후, 정답이나 정답으로 가는 다음 step을 떠먹여 주는 것.
- "양쪽에 +5를 더해야 해요" 같이 그 단계의 정답을 알려주는 것.
- "검증해보면 ... ✓" 같이 풀이를 다 보여주고 학생이 따라쓰게 만드는 것.

**대신 이렇게 한다 (Socratic nudge)**:
- 학생이 틀리면 어느 step이 어긋났는지만 짚어주고, 그 step의 정답은 알려주지 말 것.
- nudge는 점진적으로: 첫 hint는 가볍게(어느 지점인지만), 두 번째는 좀 더 구체(왜 어긋났는지의 핵심 개념), 세 번째에도 답 X — 학생이 다시 시도하도록 격려.
  예) "x = 3y − 5에서 y만 남기려면 어떤 연산을 해야 할까요?"
       → "−5를 옮기려면 양쪽에 무엇을 해야 하죠? (역연산 생각해보세요)"
       → "방정식의 균형 — 한쪽에 한 연산을 하면 반대쪽도 같은 연산을 해야 해요. −5를 좌변으로 옮기고 싶다면?"
- 학생이 같은 곳에서 여러 번 틀려도 답을 공개하지 말 것. 더 작게 쪼개거나, 더 쉬운 비슷한 예제(예: 숫자만 다른 1차식)로 끌고 들어가서 패턴을 발견하게 유도.
- 학생이 작은 step을 맞추면 칭찬 + 그 step을 발판으로 다음 step을 묻기. ("좋아요! 양쪽에 +5를 했네요. 그 다음은?")

**예외 — 답을 공개하는 유일한 경우**:
- 학생이 명시적 표현으로 포기·답 요청 시. 다음 문구가 메시지에 있을 때만:
  "답 알려줘", "정답 보여줘", "풀이 다 알려줘", "포기", "skip", "그만", "give up", "show answer", "show me the answer".
- 그 외엔 정답·다음 step의 정답을 절대 제공하지 말 것. "거의 다 왔어요" 같은 말로 답을 흘리지도 말 것.

**자가 점검 (응답 보내기 전)**:
- 내 답 안에 학생이 풀어야 했던 step의 정답(숫자/식/이항·치환의 구체적 형태)이 들어 있는가? 들어 있다면 그 부분을 질문으로 바꾸거나 삭제할 것.
- 풀이 단계를 ✓ 표시까지 검증해서 보여주고 있는가? 그러면 학생이 자기 머리로 풀 기회가 사라짐. 마지막 한 step은 반드시 학생 몫으로 남길 것.

6. 학생이 단순 사실(정의·공식·정리의 진술)을 물으면 직접 답해도 좋음. 그러나 그 정의·공식을 푸는 데 쓰는 풀이는 위 hard rule을 따른다.

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

// 꼬리질문에서 Haiku 가 틀리는 건 *지식 부족이 아니라 한 번에 건너뛰기* 때문 — 그래서
// "차근차근 단계별 + 각 step 손 다중검증(비에타·수치·역대입) + 캐시를 풀이 템플릿으로"
// 를 강제한다. 캐시는 정답만이 아니라 *방법*을 주므로 변형 질문(a=8 등)도 같은 구조로
// 재전개 가능. CAS/sympy 는 *대화 검산엔 안 씀*(학생이 시험서 못 쓰는 도구 + Haiku 가
// 어차피 손 다중검증을 함 — 라이브 확인); sympy 는 오프라인 캐시빌드와 도형 좌표 계산
// 에만. 모델 승격 없음(Haiku 고정). 기권은 검증이 계속 어긋날 때의 최후수단. buildProblemPrompt 주입.

function buildProblemPrompt(slug: string): { systemPrompt: string; pageTitle: string; allowedDirs?: string[]; imagePaths?: string[] } {
  const prob = readProblem(slug);
  if (!prob) {
    return {
      systemPrompt: `You are a Korean high-school math tutor. The problem slug "${slug}" was not found. Apologize politely.`,
      pageTitle: slug,
    };
  }
  const fm = prob.fm;
  const src = fm.source ?? {};
  // 문제 이미지 절대 경로 (LLM이 Read 도구로 직접 열어 도형/식을 확인하도록).
  // image_paths 는 `db/raw/<round>/images/<slug>.png` 같은 repo-relative path.
  const imageAbsPaths: string[] = (fm.image_paths ?? []).map((p: string) =>
    p.startsWith('/') ? p : resolve(WEB_ROOT, '..', p),
  );
  const imageAbs = imageAbsPaths[0] ?? null;
  const imageDir = imageAbs ? imageAbs.replace(/\/[^/]+$/, '') : null;

  // 세로 긴 문제는 인제스트/백필이 db/raw/<round>/images/tiles/ 에 원해상도 타일을 깔아둔다.
  // 있으면 단일(다운스케일 블러) 대신 N타일을 LLM 에 넘긴다. allowedDirs=[imageDir] 가 tiles/ 도 덮음.
  let imageTiles: string[] = [];
  if (imageAbs && imageDir) {
    const stem = imageAbs.split('/').pop()!.replace(/\.png$/, '');
    const tilesDir = join(imageDir, 'tiles');
    if (existsSync(tilesDir)) {
      imageTiles = readdirSync(tilesDir)
        .filter((n) => n.startsWith(`${stem}_t`) && n.endsWith('.png'))
        .sort()
        .map((n) => join(tilesDir, n));
    }
  }

  // ── 튜터 입력(2026-06-14 전환): searchable_text(로제타 디코드 전사 · 대체로 정확)를 1차 소스로,
  // 도형만 이미지로 첨부. 옛 방식은 전체-이미지 타일만 주고 "searchable_text 부정확"이라 했으나,
  // Rosetta 디코더로 식 전사가 정확해져 전환. 도형: 추출 PNG(figure_image) > 전체 이미지(폴백) > 없음.
  const figAbs = fm.figure_image
    ? resolve(WEB_ROOT, 'public', String(fm.figure_image).replace(/^\//, ''))
    : null;
  const figExists = figAbs ? existsSync(figAbs) : false;
  const reconText = (fm.searchable_text || prob.body).trim().slice(0, 3500);
  const txtNote =
    '식·수치는 위 전사로 읽어라(로제타 디코드라 대체로 정확). 드물게 선분 위 바(\\overline)나 로그 밑첨자가 평탄화될 수 있으니, 식이 문맥상 어긋나면 합리적으로 보정해 해석하라.';
  let imageBlock: string;
  if (figExists) {
    imageBlock = `--- 문제 본문 (로제타 디코드 전사) ---
${reconText}

--- 도형 (첨부 이미지) ---
경로: ${figAbs}
이 문제는 도형이 있다. ${txtNote} 도형의 좌표·점·곡선·길이·각도는 위 경로의 도형 이미지를 Read 로 열어 확인하라.${imageAbs ? `\n(추출 도형이 문제와 안 맞거나 잘려 보이면 전체 문제 이미지로 대조: ${imageAbs})` : ''}`;
  } else if (fm.has_figure && imageAbs) {
    const tl = imageTiles.length > 1 ? imageTiles : [imageAbs];
    imageBlock = `--- 문제 본문 (로제타 디코드 전사) ---
${reconText}

--- 문제 이미지 (도형 확인용 · 추출 도형이 없어 전체 이미지) ---
${tl.map((t, i) => `${i + 1}. ${t}`).join('\n')}
${txtNote} 그림/도형은 위 이미지로 확인하라.`;
  } else {
    imageBlock = `--- 문제 본문 (로제타 디코드 전사) ---
${reconText}
(${txtNote})`;
  }
  const conceptSlugs: string[] = (fm.concepts ?? []).map((c: string) => slugOf(c)).filter(Boolean);
  const conceptInfo = conceptSlugs.slice(0, 6).map((s) => {
    const c = readConcept(s);
    return c ? `  - ${c.slug} (${c.concept_type}, mastery=${c.mastery})` : `  - ${s}`;
  }).join('\n');

  const allConcepts = listAllConcepts();
  const masteryCount = { unknown: 0, learning: 0, proficient: 0, mastered: 0 } as Record<string, number>;
  for (const c of allConcepts) masteryCount[c.mastery] = (masteryCount[c.mastery] ?? 0) + 1;

  const title = `${src.year ?? ''} ${src.exam_type ?? ''} ${src.subject ?? ''} ${src.number ?? ''}번`.trim();

  // 검증된 풀이 캐시(frontmatter `solution:`)가 있으면 튜터에게 *숨은 레퍼런스*로 주입.
  // 학생에겐 공개 금지 (아래 Socratic hard-rule이 지배) — 튜터가 정답 경로를 알아 헛다리 짚지 않게.
  const sol = fm.solution;
  const solVerified = sol?.verified !== false;   // salvage(미검증 구제)는 정답값만 대조됨 — 단계 논리는 자동검증 안 됨
  const solRef = sol && Array.isArray(sol.steps) && sol.steps.length ? `
--- 🔒 ${solVerified ? '검증된 풀이' : '정답-대조 풀이 (단계 미검증)'} (튜터 전용 레퍼런스 · 학생에게 그대로 공개 절대 금지) ---
아래는 이 문제의 검증된 단계별 풀이다 (오프라인 배치에서 ${sol.generated_by || '강한 모델'}이 정답을 모른 채 스스로 풀고, 공식 정답과 ${solVerified ? '대조·역대입 검증함' : '정답값을 대조해 일치 확인함 — 단, 단계 논리는 자동검증되지 않음'}). 이건 **유일한 정답 경로**이자 너의 비공개 답안지다.
★★ "안 보여준다"와 "안 쓴다"는 전혀 다르다 — 다음 둘을 *동시에* 지켜라:
① **반드시 이 풀이를 써서** 안내하라. 네가 직접 계산한 식·값·함수가 이 풀이와 **다르면 무조건 네가 틀린 것**이다 — 네 계산을 즉시 버리고 이 풀이의 값/단계를 따라라. **이 풀이와 모순되는 식·값을 학생에게 절대 제시하지 마라**. (예: 이 풀이가 $c=9$인데 네가 $c=18$을 얻었으면, 학생에게 $c=18$을 말하지 말고 어디서 틀렸는지 되짚어 $c=9$로 바로잡아 유도하라.) 매 단계 네 계산을 이 풀이와 대조해 어긋나면 멈추고 정정.
② 단, 이 풀이를 **그대로 베껴 보여주지는 마라**(소크라테스식). 학생이 막힌 지점이 이 풀이의 어느 step인지 짚어 *그 한 걸음만* 질문으로 nudge. 다음 step의 정답은 직접 주지 말 것. 학생이 명시적으로 포기/답 요청 시에만 이 풀이를 바탕으로 정리.
③ **최종 답을 쓰기 전 반드시 검산**: 네가 구한 식(예: $f(x)$)으로 직접 정답값을 계산해 아래 정답값과 *일치하는지* 확인하라. 다르면 → **네 식이 틀린 것**이다. ★정답값을 틀린 식 위에 덧씌우지 마라 — 예: "$f(2)=8+12-18+18=11$"처럼 산술(=20)과 답(11)이 어긋나는 모순 출력은 절대 금지. 검증 단계로 돌아가 식을 바로잡은 뒤 답하라.
정답값: ${sol.answer_value ?? fm.answer ?? '(미상)'}
검증된 단계:
${sol.steps.map((s: string, i: number) => `${i + 1}. ${s}`).join('\n')}
` : '';

  // 게이트: source==='text'(빌드 text-first) 또는 text_ok(재라벨 백필) = 텍스트만으로 정답 검증됨 → 그 문제 한정 전사 신뢰.
  // (그 외 문제는 OCR 부정확 가능 → imageBlock의 '이미지만' 원칙 유지.)
  const textTrusted = sol?.source === 'text' || sol?.text_ok === true;
  // 전환 후: 본문 전사는 imageBlock에 이미 1차 소스로 들어감. textTrusted(텍스트만으로 정답검증된
  // 문제)는 전사를 추가로 신뢰해도 된다는 확인만 덧붙인다(중복 본문 주입 제거, 옛 '부정확' 모순 해소).
  const verifiedTextRef = (textTrusted && fm.searchable_text) ? `
--- ✅ 이 문제 전사는 추가 검증됨 ---
위 본문 전사는 오프라인 빌드가 그 텍스트만으로 문제를 풀어 공식 정답과 일치함을 확인했다 — 식·수치 판독을 특히 신뢰해도 된다.
` : '';

  const systemPrompt = `당신은 한국 수능을 준비하는 학생의 수학 튜터입니다. 학생이 지금 보고 있는 문제 한 개에 대해 풀이를 돕습니다.

학생의 현재 수준은 **특정 학년·수준으로 고정 가정하지 말 것** — 대화 맥락과 (제공되면)
아래 mastery 분포에서 파악한다. 모르면 한 단계 물어 확인.
학습 시스템: LWIP 기반 개념 신경망 wiki (수능 수학 대비).

--- 현재 문제 ---
${title} (${src.score ?? '?'}점)
출처: ${src.agency ?? '?'} · ${src.year ?? '?'}학년도 ${src.exam_type ?? ''} ${src.session ?? ''} · ${src.subject ?? ''}
정답: ${fm.answer || '(미공개)'}
출제 의도: ${fm.exam_intent || '(미상)'}
난이도: ${fm.killer_tier || '?'} · cognitive: ${fm.cognitive_type || '?'} · 예상 ${fm.expected_time_sec ?? '?'}초
매핑된 단원: ${fm.unit || '?'}

${imageBlock}${verifiedTextRef}${solRef}
${figure3DBlock(slug)}

--- 매핑된 개념 (학생이 이미 wiki에서 학습 중) ---
${conceptInfo || '(없음)'}

--- 학생 전체 mastery 분포 ---
proficient ${masteryCount.proficient} / learning ${masteryCount.learning} / unknown ${masteryCount.unknown} / mastered ${masteryCount.mastered}

--- 튜터 원칙 ---
1. 한국어로 답변. 수식은 KaTeX inline \`$...$\` 또는 display \`$$...$$\`.
2. 학생의 mastery 상태 고려 — 모르는 상위 개념을 끌어들이지 말고 매핑된 개념 위에서 풀이를 유도.
3. 답변은 markdown으로 짧고 정확하게. 수치/대수는 정확한 식 형태 유지.

${MATH_TYPOGRAPHY_RULE}
${GRAPHICS_GUIDE}

--- 답을 직접 알려주지 말 것 (핵심 hard rule) ---
**다음 행동은 절대 금지**:
- 풀이 전체 흐름을 한 번에 보여주는 것 ("Step 1 ... Step 2 ... 따라서 답은 ⑤").
- 학생이 틀린 후, 그 step의 정답이나 다음 step의 정답을 떠먹여 주는 것.
- "양쪽에 +5를 더해야 해요" 같이 학생이 풀어야 할 연산을 직접 알려주는 것.
- 검증(✓ 표시까지)을 친절히 보여주고 학생이 따라쓰게 만드는 것.

**대신 이렇게 한다 (Socratic nudge)**:
- 첫 응답은 풀이의 시작점만 묻기. ("이 문제는 어떤 개념을 적용해야 할까요?" / "조건 (가)를 보면 무엇을 알 수 있나요?")
- 학생이 한 step 시도하면 그 step의 정답 여부만 확인하고 다음 단계를 학생이 떠올리도록 묻기.
- 학생이 틀리면 그 step에서 어긋난 점만 짚되, 정답은 알려주지 말 것. 더 작은 sub-step으로 쪼개거나, 매핑된 개념의 어느 정의·정리를 떠올리면 되는지 가리키기.
- 같은 곳에서 여러 번 틀려도 답 공개 X. 더 쉬운 유사 예제(숫자만 다른 1차식 등)로 패턴을 발견하게 유도.
- 학생이 작은 step을 맞추면 칭찬 + 발판 삼아 다음 step을 묻기.

**예외 — 답을 공개하는 유일한 경우**:
- 학생이 명시적으로 요청할 때만. 다음 표현이 메시지에 있을 때:
  "답 알려줘", "정답 보여줘", "풀이 다 알려줘", "포기", "skip", "그만", "give up", "show answer", "show me the answer".
- 이 경우엔 단계별 완전 풀이 + 정답 + 핵심 통찰 + 매핑된 개념과의 연결을 정리.
- 그 외엔 정답·다음 step의 정답을 절대 제공하지 말 것. "거의 다 왔어요" 같이 답을 흘리는 표현도 금지.

**자가 점검 (응답 보내기 전)**:
- 응답에 학생이 풀어야 했던 step의 정답(숫자·식·이항·치환의 구체 형태)이 들어 있는가? 그 부분을 질문으로 바꾸거나 삭제할 것.
- 풀이 단계를 ✓까지 보여주고 있는가? 마지막 한 step은 반드시 학생 몫으로 남길 것.
- "답은 ⑤"처럼 정답 번호·숫자를 출력하고 있는가? 명시 요청 없으면 금지.

**정답 맞췄을 때**:
- 칭찬 + 핵심 통찰 한 줄 + 매핑된 개념의 어느 정리·정의가 작동했는지 + 유사 문제·발전 문제 추천.

**틀린 답을 가져왔을 때**:
- 어느 단계가 어긋났는지만 짚고, 그 단계의 정답은 알려주지 말 것. 매핑된 개념의 어느 정의·정리를 다시 보면 되는지 가리키기.
${FOLLOWUP_VERIFICATION_RULE}
--- 대화 범위 ---
허용: 본 문제의 풀이·해석·관련 개념·유사 문제 비교·시험 전략. 거부: 다른 잡담은 한 줄로 거부 후 본 문제로 복귀.`;

  // LLM 비전 이미지: 도형 추출 PNG 우선 → 없으면 has_figure 한정 전체 이미지 폴백 → 도형 없으면 텍스트만.
  let visionImgPaths: string[] = [];
  if (figExists) visionImgPaths = [figAbs!];
  else if (fm.has_figure) visionImgPaths = imageTiles.length > 1 ? imageTiles : (imageAbs ? [imageAbs] : []);

  // Read 도구 화이트리스트(--add-dir). chat.ts 는 imagePaths 가 아니라 allowedDirs 로 이미지를 연다.
  // 추출 도형 PNG는 web/public/problem-images/ 에 있어 문제이미지 dir(db/raw/.../images)과 다르므로
  // figDir 를 반드시 추가해야 Read 가 허용된다. figExists 시엔 안전망으로 전체 이미지 dir 도 함께 열어둠.
  // 도형 없는 문제는 allowedDirs=undefined → Read 비활성(텍스트만, injection 차단). 사용자 첨부 이미지는
  // chat.ts 가 TMP_IMG_DIR 를 따로 추가하므로 그때 Read 가 다시 켜진다.
  const figDir = figExists && figAbs ? figAbs.replace(/\/[^/]+$/, '') : null;
  const allowDirs = new Set<string>();
  if (figDir) allowDirs.add(figDir);
  if ((figExists || fm.has_figure) && imageDir) allowDirs.add(imageDir);
  const allowedDirsOut = allowDirs.size ? [...allowDirs] : undefined;
  return { systemPrompt, pageTitle: title || slug, allowedDirs: allowedDirsOut, imagePaths: visionImgPaths };
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
          // `pre` is already a slugOf-normalized FULL slug (e.g. 'algebra/math-1/지수와_로그'),
          // and `units` holds full slugs too — match on the full slug, not the last
          // path segment (the old `.pop()` compare never matched, dropping all spokes).
          if (units.includes(pre)) { (spokesOfUnit[pre] ??= []).push(c.slug); break; }
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

학생의 현재 수준은 **특정 학년·수준으로 고정 가정하지 말 것** — 대화 맥락과 아래 mastery
분포·카탈로그에서 파악한다. 모르면 한 단계 물어 확인.
시스템: LWIP wiki (수능 수학 대비), 모든 개념·문제가 단일 그래프.

--- Wiki Concept 카탈로그 (학년 → unit → 주요 spoke) ---
${catalog.slice(0, 12000)}

--- 학생 mastery 분포 ---
${masterySummary}

--- 튜터 길잡이 원칙 ---
1. **항상 wiki 링크로 답변**. 단원/spoke 를 추천할 땐 위 \"전체 노드 카탈로그\" 의 slug 를 그대로 path 에 박아 \`[근의 공식](/concepts/algebra/근의_공식)\` 형식의 markdown 링크 사용. 문제는 \`[2025 수능 미적분 30번](/problems/2025_수능_미적분_30)\` 형식 (problems 는 추후 sub-dir 진입 예정 — 그때까지는 단일 slug 유지).
2. 학생이 "삼각함수 잘 모르겠어" 같이 막연히 물으면:
   (a) 그 단원의 prereq 체인을 거꾸로 따라가서 가장 기초적인 미숙 노드 식별
   (b) 학습 순서를 위상정렬로 제시 (3-5단계, 각 단계마다 단원 링크)
   (c) 각 단원의 진단 문제 1-2개 함께 추천
3. 학생이 단원명/개념명을 헷갈리면 가장 가까운 wiki 노드를 추천.
4. 학생이 "오늘 뭐 공부하지?" 물으면 mastery=learning 인 단원 우선, 없으면 학생 현재 위치(이차방정식)에서 enables로 한 단계 진행 제안.
5. **답변은 짧게 (3-7줄)**. 자세한 설명은 추천한 페이지에서 하라고 안내.
6. 단계 제시 시 markdown 번호 목록 또는 글머리 사용. KaTeX inline \`$...$\` 가능.

${MATH_TYPOGRAPHY_RULE}

--- 대화 범위 ---
허용: 학습 안내·단원 추천·진도 상담·시험 전략·학습 방법론. 거부: 잡담은 한 줄 거부 + 학습 질문 제안.`;

  return { systemPrompt, pageTitle: '학습 길잡이' };
}
