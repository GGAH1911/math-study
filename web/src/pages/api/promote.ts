import type { APIRoute } from 'astro';
import { writeFileSync, mkdirSync, existsSync, appendFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

export const prerender = false;

const WEB_ROOT = process.cwd();
const SYNTHESES_DIR = resolve(WEB_ROOT, '..', 'docs', 'syntheses');
const LOG_PATH = resolve(WEB_ROOT, '..', 'docs', 'log.md');

type PromoteBody = {
  slug: string;            // origin concept slug (page where chat happened)
  question: string;        // student's question
  answer: string;          // tutor's answer (markdown)
  title?: string;          // optional manual title
};

function sanitizeFilename(s: string): string {
  return s.replace(/[^\w가-힣ㄱ-ㅎㅏ-ㅣ_-]/g, '_').slice(0, 60);
}

// LLM-generated math frequently:
//   1) uses `\begin{align}` (standard LaTeX, unsupported by KaTeX —
//      rewrite to `aligned`).
//   2) puts `$$` on the same line as content, which trips remark-math
//      into parsing it as inline math and swallowing the next paragraph.
//      Move display `$$` onto its own line so remark-math sees a clean
//      display-math block.
// Both fixes happen at write time so the persisted markdown is correct
// regardless of which downstream renderer reads it (Astro MDX, in-chat
// applyKatex, raw `cat` of the file).
function normalizeChatMarkdown(s: string): string {
  let out = s
    .replace(/\\begin\{align\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{align\*?\}/g, '\\end{aligned}')
    .replace(/\\begin\{eqnarray\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{eqnarray\*?\}/g, '\\end{aligned}');
  // `$$content` (no newline after) → `$$\ncontent`
  // NOTE: in a String.replace replacement, `$$` denotes a literal single `$`,
  // so use a function replacer to emit a real `$$` and avoid corrupting the
  // display delimiter into a single `$`.
  out = out.replace(/(\$\$)(?=\S)/g, () => '$$\n');
  // `content$$` (no newline before) → `content\n$$`
  out = out.replace(/(\S)(\$\$)/g, (_m, p1) => `${p1}\n$$`);
  return out;
}

// body.title 이 슬러그 경로( `logic/high-1/집합과_명제/논리` 또는
// `학습 노트 - <경로>` )를 그대로 담고 오는 경우가 있어 H1 에 raw 경로가
// 박힌다. 경로형이면 마지막 segment 만 사람이 읽는 leaf 라벨로 축약하고
// (`_`→공백), 일반 제목은 손대지 않는다.
function humanizeTitle(title: string): string {
  // `학습 노트 - <경로>` prefix 분리(있으면 보존).
  const m = title.match(/^(\s*학습 노트\s*-\s*)(.+)$/);
  const prefix = m ? m[1] : '';
  const rest = m ? m[2] : title;
  // 슬래시로 나뉜 영문/언더스코어 세그먼트(예: high-1, 집합과_명제) → 경로형.
  if (rest.includes('/')) {
    const leaf = rest.split('/').filter(Boolean).pop() ?? rest;
    return `${prefix}${leaf.replace(/_/g, ' ')}`;
  }
  return title;
}

// 출처 blockquote 링크의 '텍스트'만 읽기 좋게: `/`→` › `, `_`→공백.
// href/URL(괄호 안 경로)은 라우팅용이라 절대 건드리지 않는다.
function humanizeSlugLabel(slug: string): string {
  return slug.replace(/\//g, ' › ').replace(/_/g, ' ');
}

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

export const POST: APIRoute = async ({ request, locals }) => {
  if (!locals.user) return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'content-type': 'application/json' } });
  const body = (await request.json()) as PromoteBody;
  if (!body.slug || !body.question || !body.answer) {
    return new Response(JSON.stringify({ error: 'slug + question + answer required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  if (body.slug.includes('..') || /\\/.test(body.slug)) {
    return new Response(JSON.stringify({ error: 'invalid slug' }), { status: 400 });
  }

  const date = todayISO();
  const titleStub = sanitizeFilename(body.title ?? body.question.slice(0, 40));
  // synthesis 파일명에는 sub-dir `/` 가 들어가면 안 되므로 마지막 segment 만 사용.
  const slugLeaf = body.slug.split('/').pop() ?? body.slug;
  const filename = `${date}_${slugLeaf}_${titleStub}.md`;
  mkdirSync(SYNTHESES_DIR, { recursive: true });
  const filepath = join(SYNTHESES_DIR, filename);
  if (existsSync(filepath)) {
    return new Response(JSON.stringify({ error: 'file exists', path: filepath }), {
      status: 409,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const content = `---
sources: [chat with claude-haiku-4-5 on ${date}]
created: ${date}
updated: ${date}
origin_concept: docs/concepts/${body.slug}.md
promoted_from: chat
review_state: new
next_review: ${date}
---

# ${body.title ? humanizeTitle(body.title) : body.question.slice(0, 60)}

> **출처**: [${humanizeSlugLabel(body.slug)}](../concepts/${body.slug}.md) 페이지에서 진행한 LLM 튜터 대화를 영구 wiki 노드로 promote (LWIP Query & Promote, lifecycle.md §Query-Promote).

## 질문

${normalizeChatMarkdown(body.question)}

## 답변

${normalizeChatMarkdown(body.answer)}

---
*Promoted ${date}. 사용자가 wiki에 영구화한 답변.*
`;

  writeFileSync(filepath, content, 'utf-8');

  // Append to log
  try {
    appendFileSync(LOG_PATH, `\n## [${date}] promote | chat → synthesis: "${body.question.slice(0, 60)}" from ${body.slug}\n`);
  } catch { /* non-fatal */ }

  return new Response(JSON.stringify({
    ok: true,
    path: `docs/syntheses/${filename}`,
    slug: filename.replace(/\.md$/, ''),
  }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};
