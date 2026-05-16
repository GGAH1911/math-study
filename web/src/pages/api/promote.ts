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

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

export const POST: APIRoute = async ({ request }) => {
  const body = (await request.json()) as PromoteBody;
  if (!body.slug || !body.question || !body.answer) {
    return new Response(JSON.stringify({ error: 'slug + question + answer required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const date = todayISO();
  const titleStub = sanitizeFilename(body.title ?? body.question.slice(0, 40));
  const filename = `${date}_${body.slug}_${titleStub}.md`;
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

# ${body.title ?? body.question.slice(0, 60)}

> **출처**: [${body.slug.replace(/_/g, ' ')}](../concepts/${body.slug}.md) 페이지에서 진행한 LLM 튜터 대화를 영구 wiki 노드로 promote (LWIP Query & Promote, lifecycle.md §Query-Promote).

## 질문

${body.question}

## 답변

${body.answer}

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
