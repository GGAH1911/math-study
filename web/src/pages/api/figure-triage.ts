import type { APIRoute } from 'astro';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const prerender = false;

const IDX = fileURLToPath(new URL('../../data/figure-triage.json', import.meta.url));
const STATUSES = ['untriaged', 'reuse', 'redraw-2d', 'redraw-3d'];

function json(d: unknown, s = 200): Response {
  return new Response(JSON.stringify(d), { status: s, headers: { 'content-type': 'application/json' } });
}

// POST { image, status, notes? } → 트리아지 분류 저장 (admin only; /dev/* 와 함께 middleware 게이팅)
export const POST: APIRoute = async ({ request, locals }) => {
  const user = (locals as { user?: { is_admin?: boolean; email?: string } }).user;
  if (!user?.is_admin) return json({ error: 'forbidden' }, 403);

  let body: { image?: string; status?: string; notes?: string };
  try { body = await request.json(); } catch { return json({ error: 'invalid json' }, 400); }
  const { image, status, notes } = body;
  if (!image || !status || !STATUSES.includes(status)) return json({ error: 'bad params' }, 400);

  let idx: { figures: Record<string, Record<string, unknown>> };
  try { idx = JSON.parse(readFileSync(IDX, 'utf-8')); } catch { return json({ error: 'index missing' }, 500); }
  const f = idx.figures[image];
  if (!f) return json({ error: 'figure not found' }, 404);

  f.status = status;
  if (notes !== undefined) f.notes = notes || null;
  f.triaged_by = user.email ?? 'admin';
  f.triaged_at = new Date().toISOString();
  writeFileSync(IDX, JSON.stringify(idx, null, 2));
  return json({ ok: true, figure: f });
};
