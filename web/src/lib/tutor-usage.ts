// 튜터 LLM 사용량·캐시 메트릭을 계정별로 DB(tutor_usage)에 적재. chat.ts 의 stream-json result
// 이벤트 usage 에서 추출해 호출. best-effort(실패해도 채팅엔 영향 0). 조회는 SQL — docs/ops/status/db-metrics.md.
import sql from './db.ts';

export type TutorUsage = {
  userId?: string | null;
  collection?: string | null;
  slug?: string | null;
  model?: string | null;
  byok?: boolean;
  inputTokens?: number;
  outputTokens?: number;
  cacheReadTokens?: number;
  cacheCreationTokens?: number;
};

// claude stream-json 의 result 이벤트 usage(또는 그 형태) → 정수 메트릭.
export function parseUsage(usage: Record<string, unknown> | undefined | null): {
  inputTokens: number; outputTokens: number; cacheReadTokens: number; cacheCreationTokens: number;
} | null {
  if (!usage || typeof usage !== 'object') return null;
  const n = (k: string) => (typeof usage[k] === 'number' ? (usage[k] as number) : 0);
  return {
    inputTokens: n('input_tokens'),
    outputTokens: n('output_tokens'),
    cacheReadTokens: n('cache_read_input_tokens'),
    cacheCreationTokens: n('cache_creation_input_tokens'),
  };
}

export async function logTutorUsage(u: TutorUsage): Promise<void> {
  try {
    // user_id 가 users 에 실재할 때만 FK 충족 — 합성/미인증(noauth dev·삭제된 계정)은 NULL 로 적재해
    //   메트릭 자체는 보존(FK 위반으로 행 전체가 버려지지 않게).
    let uid = u.userId ?? null;
    if (uid) {
      const exists = await sql`SELECT 1 FROM users WHERE id = ${uid} LIMIT 1`;
      if (exists.length === 0) uid = null;
    }
    await sql`
      INSERT INTO tutor_usage (user_id, collection, slug, model, byok, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens)
      VALUES (${uid}, ${u.collection ?? null}, ${u.slug ?? null}, ${u.model ?? null}, ${u.byok ?? false},
              ${u.inputTokens ?? 0}, ${u.outputTokens ?? 0}, ${u.cacheReadTokens ?? 0}, ${u.cacheCreationTokens ?? 0})
    `;
  } catch (e) {
    // best-effort — DB 실패가 채팅 응답을 막지 않게 삼킨다.
    console.error('[tutor_usage] insert failed:', (e as Error).message);
  }
}
