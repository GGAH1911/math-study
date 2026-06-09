// POST /api/mastery-promote  {slug, to, reason?, evidence?}
// 멀티유저: mastery 를 frontmatter(전역)가 아니라 concept_mastery(로그인 사용자별)에 UPSERT.
// slug 는 concept_id(중첩 slug). 존재하는 개념인지 .md 파일로 검증만 하고 파일은 안 건드림.
import type { APIRoute } from 'astro';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { promoteMastery, MASTERY_LEVELS, type MasteryLevel } from '../../lib/mastery.ts';

export const prerender = false;

const CONCEPTS_DIR = resolve(process.cwd(), '..', 'docs', 'concepts');

type Body = { slug: string; to: MasteryLevel; reason?: string; evidence?: string[] };

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}
function todayISO(): string { return new Date().toISOString().slice(0, 10); }

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);

  let body: Body;
  try { body = (await request.json()) as Body; }
  catch { return json({ error: 'invalid JSON body' }, 400); }

  if (!body.slug || !body.to) return json({ error: 'slug + to required' }, 400);
  if (!MASTERY_LEVELS.includes(body.to)) {
    return json({ error: `to must be one of ${MASTERY_LEVELS.join(', ')}` }, 400);
  }
  // sub-dir slug 허용. `..`·backslash 차단.
  if (/\\/.test(body.slug) || body.slug.includes('..') || !/^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/.test(body.slug)) {
    return json({ error: 'invalid slug' }, 400);
  }

  // 실존 개념인지 검증(파일 존재). 경로 탈출 방지. 파일은 쓰지 않는다.
  const filepath = resolve(CONCEPTS_DIR, `${body.slug}.md`);
  if (!filepath.startsWith(resolve(CONCEPTS_DIR) + '/')) return json({ error: 'path escape' }, 400);
  if (!existsSync(filepath)) return json({ error: 'concept not found' }, 404);

  const newEvidence: string[] = [];
  if (body.reason) newEvidence.push(`chat-judgment @ ${todayISO()}: ${body.reason}`);
  if (Array.isArray(body.evidence)) for (const e of body.evidence) if (typeof e === 'string') newEvidence.push(e);

  try {
    const { from, to } = await promoteMastery(userId, body.slug, body.to, newEvidence);
    return json({ ok: true, from, to, slug: body.slug });
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
};
