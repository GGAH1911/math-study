// 헬스체크 — PaaS(Railway/Render) 컨테이너 readiness/liveness 프로브용.
// GET /api/health        → { status, db, uptime } 200(정상) | 503(DB 불통).  ← 프로브가 매초 때리는 경로, 가볍게 유지
// GET /api/health?deep=1 → 위 + 튜터 백엔드 **실호출**(LLM 한 번). 느리고 과금되니 프로브가 아니라
//                          크론·수동 점검용. 실패해도 200(status='degraded')이 아니라 503 을 준다.
// middleware PUBLIC_PATHS 에 /api/health 가 이미 있어 미인증 접근 가능.
//
// ★deep 이 필요한 이유(2026-08-12 사고): ~/.claude/.credentials.json 의 OAuth 블록이 조용히 사라져
//   `claude -p` 가 'Not logged in' 이 되면서 **튜터가 15시간 죽어 있었다**. 그동안 이 엔드포인트는
//   내내 200 이었고 컨테이너도 healthy 였다 — DB 만 봤기 때문이다. 제품의 핵심 기능이 죽었는데
//   어떤 신호도 없었다. 그래서 "튜터가 실제로 답하는가"를 직접 확인하는 경로를 따로 둔다.
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';
import { streamNousTutor, nousConfigured } from '../../lib/tutor/nous-stream.ts';

export const prerender = false;

/** 튜터 백엔드에 최소 프롬프트를 던져 실제로 토큰이 나오는지 본다. */
async function probeTutor(timeoutMs = 25_000): Promise<{ tutor: 'ok' | 'down' | 'unconfigured'; detail?: string; ms?: number }> {
  if (!nousConfigured()) return { tutor: 'unconfigured' };
  const t0 = Date.now();
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), timeoutMs);
  let text = '';
  let err: string | undefined;
  try {
    await streamNousTutor(
      {
        // 시스템 프롬프트를 짧게 둔다 — 캐시 경계를 건드리지 않고, 과금도 최소로.
        systemPrompt: 'You are a health probe. Answer with a single digit only.',
        userPrompt: '1+1=?',
        maxTokens: 8,
        idleMs: timeoutMs,
        signal: ac.signal,
      },
      { onDelta: (t) => { text += t; }, onError: (m) => { err = m; }, onDone: () => {} },
    );
  } catch (e) {
    err = e instanceof Error ? e.message : String(e);
  }
  clearTimeout(timer);
  const ms = Date.now() - t0;
  if (text.trim().length > 0) return { tutor: 'ok', ms };
  return { tutor: 'down', detail: err ?? '빈 응답', ms };
}

export const GET: APIRoute = async ({ url }) => {
  let db: 'ok' | 'down' = 'down';
  let dbError: string | undefined;
  try {
    // 가벼운 라운드트립. 풀에서 커넥션 하나 빌려 SELECT 1.
    await sql`SELECT 1`;
    db = 'ok';
  } catch (e) {
    dbError = e instanceof Error ? e.message : String(e);
  }

  const deep = url.searchParams.get('deep') === '1';
  const t = deep ? await probeTutor() : null;

  // unconfigured 는 실패로 치지 않는다(키 없이 구독 폴백으로 도는 개발 환경).
  const tutorOk = !t || t.tutor === 'ok' || t.tutor === 'unconfigured';
  const ok = db === 'ok' && tutorOk;
  return new Response(
    JSON.stringify({
      status: ok ? 'ok' : 'degraded',
      db,
      ...(dbError ? { db_error: dbError } : {}),
      ...(t ? { tutor: t.tutor, ...(t.ms ? { tutor_ms: t.ms } : {}), ...(t.detail ? { tutor_error: t.detail } : {}) } : {}),
      uptime: Math.round(process.uptime()),
      ts: new Date().toISOString(),
    }),
    {
      status: ok ? 200 : 503,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    },
  );
};
