import type { APIRoute } from 'astro';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const prerender = false;

const IDX = fileURLToPath(new URL('../../data/figure-triage.json', import.meta.url));
const STATUSES = ['untriaged', 'reuse', 'redraw-2d', 'redraw-3d', 'delete'];

function json(d: unknown, s = 200): Response {
  return new Response(JSON.stringify(d), { status: s, headers: { 'content-type': 'application/json' } });
}

// POST { image, status, notes? } → 트리아지 분류 저장 (admin only; /dev/* 와 함께 middleware 게이팅)
export const POST: APIRoute = async ({ request, locals }) => {
  const user = (locals as { user?: { is_admin?: boolean; email?: string } }).user;
  if (!user?.is_admin) return json({ error: 'forbidden' }, 403);

  let body: { image?: string; status?: string; notes?: string; bulk?: boolean; sug?: string; subj?: string };
  try { body = await request.json(); } catch { return json({ error: 'invalid json' }, 400); }

  let idx: { figures: Record<string, Record<string, unknown>> };
  try { idx = JSON.parse(readFileSync(IDX, 'utf-8')); } catch { return json({ error: 'index missing' }, 500); }
  const now = new Date().toISOString();
  const who = user.email ?? 'admin';

  // 일괄 수락: { bulk:true, sug, subj? } → 미분류 중 제안=sug 인 figure 를 status=제안값으로 일괄(이미 분류된 건 보존)
  if (body.bulk) {
    const { sug, subj } = body;
    if (!sug || !STATUSES.includes(sug)) return json({ error: 'bad sug' }, 400);
    let n = 0;
    for (const f of Object.values(idx.figures)) {
      if (f.suggested === sug && f.status === 'untriaged' && (!subj || subj === 'all' || f.subject === subj)) {
        f.status = sug; f.triaged_by = who; f.triaged_at = now; n++;
      }
    }
    writeFileSync(IDX, JSON.stringify(idx, null, 2));
    return json({ ok: true, accepted: n });
  }

  // 단건
  const { image, status, notes } = body;
  if (!image || !status || !STATUSES.includes(status)) return json({ error: 'bad params' }, 400);
  const f = idx.figures[image];
  if (!f) return json({ error: 'figure not found' }, 404);
  f.status = status;
  if (notes !== undefined) f.notes = notes || null;
  f.triaged_by = who;
  f.triaged_at = now;
  writeFileSync(IDX, JSON.stringify(idx, null, 2));
  return json({ ok: true, figure: f });
};
