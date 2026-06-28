import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { tmpdir } from 'node:os';
import matter from 'gray-matter';

export const prerender = false;

// ★claude -p 캐시 친화: 레포 cwd면 git status가 시스템 프롬프트 env 블록을 매 요청 바꿔 캐시를 깬다.
//   깨끗한 빈 cwd에서 spawn → prefix 안정 → cache_read 생존. 파일접근 없어(프롬프트 임베드) 안전.
const CLEAN_DIR = process.env.CLAUDE_P_CWD || join(tmpdir(), 'claude_p_clean');
try { if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true }); } catch { /* */ }

const WEB_ROOT = process.cwd();
const DOCS = resolve(WEB_ROOT, '..', 'docs', 'concepts');
const SYNTHESES_DIR = resolve(WEB_ROOT, '..', 'docs', 'syntheses');

// Pull every synthesis whose frontmatter `origin_concept` points at this
// concept slug. Used when `useNotes: true` so the regenerated body can
// reflect what the student actually struggled with / found intuitive
// during their chat-promote history.
function loadSynthesesFor(slug: string): { title: string; body: string }[] {
  if (!existsSync(SYNTHESES_DIR)) return [];
  const target = `docs/concepts/${slug}.md`;
  const out: { title: string; body: string }[] = [];
  for (const f of readdirSync(SYNTHESES_DIR)) {
    if (!f.endsWith('.md')) continue;
    const raw = readFileSync(join(SYNTHESES_DIR, f), 'utf-8');
    const parsed = matter(raw);
    if (parsed.data?.origin_concept !== target) continue;
    const titleMatch = parsed.content.match(/^#\s+(.+?)\s*$/m);
    out.push({
      title: (titleMatch?.[1] ?? f.replace(/\.md$/, '')).trim(),
      // 본문 전체를 그대로 — 노트 자체가 짧고(~수백자) LLM 컨텍스트 한도 안.
      body: parsed.content.trim(),
    });
  }
  return out;
}

const TUTOR_SYSTEM = `당신은 한국 수능을 준비하는 학생용 수학 wiki의 콘텐츠 라이터입니다.
개념 페이지(정의/정리/예제) 하나의 '본문' 섹션을 작성합니다.

요구사항:
1. 한국어로. 한국 고등학교 교육과정 용어 우선.
2. 수식은 KaTeX inline \`$...$\` 또는 display \`$$...$$\`로. ★가독성:
   - **긴 등식/부등식 체인**(예: \`lim... = lim... = L\`, 3중 부등식 \`a ≤ b ≤ c\`)은 인라인이 아니라 **\`$$...$$\` 블록**으로 빼라(문장 중간에 넣으면 줄바꿈으로 쪼개져 읽기 어렵다).
   - **인라인 분수**는 \`\\frac\` 대신 \`\\tfrac\`(작은 분수)을 써라(인라인에서 \\frac 은 줄높이를 키워 줄간격이 들쭉날쭉해진다). 블록 \`$$\` 안에서는 \`\\dfrac\`/\`\\frac\` 정상.
3. 200-400 단어 분량.
4. 구조:
   - 정의: 정의 자체를 첫 문단에 소제목 없이 바로 서술 → ### 직관과 기하적 의미 → ### 기본 성질
   - 정리: ### 진술 + 가정 → ### 간단한 유도/증명 스케치 → ### 의의/응용
   - 예제: ### 문제 → ### 단계별 풀이 → ### 답 → ### 변형/주의
5. h1, h2 헤더 절대 사용 금지. h3(###) 이하만.
6. 검산 가능한 수치 예제는 sympy 코드 한 줄 포함 가능.
7. 출력은 본문 마크다운만. "본문:" 같은 라벨 금지. ★"정확한 진술" 소제목 절대 금지 — 정의/핵심 진술은 첫 문단에 소제목 없이 바로 쓴다.
8. ★사용자에게 보이는 글이다. 자연스러운 한국어만 쓰고 개발 용어·영문 표기를 본문에 노출하지 말 것
   (definition/theorem/example, spoke, mastery, concept_gap, Phase, LWIP 같은 단어 금지).
9. ★절대 학생에게 되묻지 말 것. "어떤 개념인지 확인이 필요합니다", "정보가 누락되어 있습니다"
   같은 질문·요청을 본문으로 쓰지 마라. 제목이 모호하면 제목·단원·선수개념으로 가장 합리적인
   표준 교육과정 개념을 스스로 판단해 그 본문을 바로 작성하라.`;

type RegenerateRequest = {
  slug: string;
  model?: 'haiku' | 'sonnet';
  // When true, append the user's promoted syntheses for this concept to
  // the user prompt as personalization hints. Defaults to false to keep
  // the existing `haiku/sonnet` buttons identical to today's behavior.
  useNotes?: boolean;
};

function fmField(text: string, key: string): string {
  const m = text.match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
  return m ? m[1].trim() : '';
}

function listField(text: string, key: string): string[] {
  const m = text.match(new RegExp(`^${key}:\\s*\\[(.*?)\\]`, 'm'));
  if (!m || !m[1].trim()) return [];
  return m[1].split(',').map((s) => s.trim()).filter(Boolean);
}

export const POST: APIRoute = async ({ request, locals }) => {
  if (!locals.user) return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'content-type': 'application/json' } });
  const { slug, model = 'haiku', useNotes = false } = (await request.json()) as RegenerateRequest;
  // sub-dir slug 허용. `..` 와 backslash 차단.
  if (!slug || /\\|\.\./.test(slug) || !/^[\w가-힣/-]+$/.test(slug)) {
    return new Response(JSON.stringify({ error: 'invalid slug' }), { status: 400 });
  }
  const file = resolve(DOCS, `${slug}.md`);
  if (!file.startsWith(resolve(DOCS) + '/')) {
    return new Response(JSON.stringify({ error: 'path escape' }), { status: 400 });
  }
  let text: string;
  try {
    text = readFileSync(file, 'utf-8');
  } catch {
    return new Response(JSON.stringify({ error: 'spoke not found' }), { status: 404 });
  }

  const parsed = matter(text);
  const ctype = (parsed.data.concept_type as string) ?? '';
  if (ctype === 'unit') {
    return new Response(JSON.stringify({ error: 'unit pages do not regenerate' }), { status: 400 });
  }

  const grade = fmField(text, 'grade');
  const unit = fmField(text, 'unit');
  const prereqs = listField(text, 'prerequisites');
  const briefMatch = text.match(/## 요약\s*\n([^\n#]+)/);
  const brief = briefMatch ? briefMatch[1].trim() : '';
  const preLabels = prereqs.map((p) => p.split('/').pop()?.replace(/\.md$/, '').replace(/_/g, ' ')).join(', ') || '없음';

  let userPrompt = `다음 개념 페이지의 본문을 작성하세요.

페이지 제목: ${slug.replace(/_/g, ' ')}
타입: ${ctype}
학년: ${grade}
소속 단원: ${unit}
선수 개념: ${preLabels}
페이지 요약(1줄): ${brief}

이 spoke를 처음 보는 학생에게 친절하면서도 정확하게 설명해 주세요. h3(###) 이하 헤더만. 출력은 markdown 본문만.`;

  // 학생의 promote된 노트를 컨텍스트로 끼워 넣어 "맞춤형 본문" 생성.
  // 노트가 0개면 일반 모드와 동일하게 진행.
  if (useNotes) {
    const notes = loadSynthesesFor(slug);
    if (notes.length > 0) {
      const noteBlock = notes
        .map((n, i) => `### [노트 ${i + 1}] ${n.title}\n${n.body}`)
        .join('\n\n---\n\n');
      userPrompt += `

---

추가 컨텍스트: 이 페이지에서 학생이 LLM 튜터와 대화한 뒤 promote한 학습 노트 ${notes.length}개입니다.
노트는 학생이 헷갈렸던 부분·와닿은 직관·복습 포인트를 압축한 결과물이라 본문 개인화에 활용 가능합니다.

활용 지침:
- 표준 본문 구조(### 정확한 진술 / ### 직관 / ### 한 줄 예 등)는 유지.
- 학생이 노트에서 헷갈렸다고 표시한 지점은 본문에서 추가 설명·예시로 보강.
- 학생에게 와닿은 직관·비유가 있다면 본문에 자연스럽게 녹임.
- 노트를 통째로 복붙하지 말 것 — 본문은 wiki 노드, 노트는 학습 기록.
- 노트와 본문 표준 내용이 충돌하면 표준 내용(정의·정리·교과 표기)이 우선.

${noteBlock}`;
    }
  }

  return new Promise<Response>((resolveResp) => {
    const child = spawn('claude', [
      '-p',
      '--model', model,
      '--max-turns', '1',
      '--output-format', 'text',
      '--no-session-persistence',
      '--system-prompt', TUTOR_SYSTEM,
      userPrompt,
    ], { env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' }, cwd: CLEAN_DIR });   // ★clean cwd(벨트)+DISABLE_GIT(멜빵) → 프롬프트 캐시 생존

    let buf = '';
    child.stdout.on('data', (c) => { buf += c.toString('utf-8'); });
    let err = '';
    child.stderr.on('data', (c) => { err += c.toString('utf-8'); });

    child.on('close', (code) => {
      if (code !== 0 || !buf.trim()) {
        resolveResp(new Response(JSON.stringify({ error: 'claude failed', stderr: err.slice(0, 500) }), { status: 500 }));
        return;
      }
      let body = buf.trim();
      // Drop accidental h1/h2 prefix
      body = body.replace(/^\s*#{1,2}\s+[^\n]+\n+/, '');

      // Splice into the spoke file. Use a lookahead end-anchor so `## 본문`
      // being the *last* section (no following `\n## ` header) still matches
      // and gets replaced in-place — otherwise the fallback below appended a
      // duplicate `## 본문` and left the stale body untouched.
      const splicePattern = /(## 본문[^\n]*\n)([\s\S]*?)(?=\n## |\s*$)/;
      let newText: string;
      if (splicePattern.test(text)) {
        newText = text.replace(splicePattern, (_, h) => `${h}\n${body}\n`);
      } else {
        const checkIdx = text.indexOf('## 학습 체크');
        if (checkIdx >= 0) {
          newText = text.slice(0, checkIdx) + '## 본문\n\n' + body + '\n\n' + text.slice(checkIdx);
        } else {
          newText = text.trimEnd() + '\n\n## 본문\n\n' + body + '\n';
        }
      }
      // Mark auto_explained: true
      if (/^auto_explained:/m.test(newText)) {
        newText = newText.replace(/^auto_explained:.*$/m, 'auto_explained: true');
      } else {
        newText = newText.replace(/^(updated:.*)$/m, '$1\nauto_explained: true');
      }
      try {
        writeFileSync(file, newText, 'utf-8');
      } catch (e) {
        resolveResp(new Response(JSON.stringify({ error: 'write failed', message: (e as Error).message }), { status: 500 }));
        return;
      }
      resolveResp(new Response(JSON.stringify({ ok: true, slug, length: body.length }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }));
    });

    child.on('error', (e) => {
      resolveResp(new Response(JSON.stringify({ error: 'spawn failed', message: e.message }), { status: 500 }));
    });
  });
};
