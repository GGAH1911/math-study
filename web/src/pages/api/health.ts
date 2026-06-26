// 헬스체크 — PaaS(Railway/Render) 컨테이너 readiness/liveness 프로브용.
// GET /api/health → { status, db, uptime } 200(정상) | 503(DB 불통).
// middleware PUBLIC_PATHS 에 /api/health 가 이미 있어 미인증 접근 가능.
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';

export const prerender = false;

export const GET: APIRoute = async () => {
  let db: 'ok' | 'down' = 'down';
  let dbError: string | undefined;
  try {
    // 가벼운 라운드트립. 풀에서 커넥션 하나 빌려 SELECT 1.
    await sql`SELECT 1`;
    db = 'ok';
  } catch (e) {
    dbError = e instanceof Error ? e.message : String(e);
  }

  const ok = db === 'ok';
  return new Response(
    JSON.stringify({
      status: ok ? 'ok' : 'degraded',
      db,
      ...(dbError ? { db_error: dbError } : {}),
      uptime: Math.round(process.uptime()),
      ts: new Date().toISOString(),
    }),
    {
      status: ok ? 200 : 503,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    },
  );
};
