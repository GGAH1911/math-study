// Server-side Postgres client. Single connection pool per Node process.
// This file is only imported from `prerender = false` API routes, never from
// pages built at compile time.
import postgres from 'postgres';

const DATABASE_URL =
  process.env.MATH_STUDY_DATABASE_URL ??
  'postgresql://mathstudy:mathstudy@127.0.0.1:5434/mathstudy';

// Single-user system. The schema requires user_id NOT NULL on every state
// row, so we mint one stable UUID and use it everywhere. Override via env
// if/when multi-user lands.
export const SINGLE_USER_ID =
  process.env.MATH_STUDY_USER_ID ??
  '00000000-0000-0000-0000-000000000001';

// Module-level singleton — postgres.js manages an internal connection pool.
declare global {
  // eslint-disable-next-line no-var
  var __mathStudySql: ReturnType<typeof postgres> | undefined;
}
const sql =
  globalThis.__mathStudySql ??
  postgres(DATABASE_URL, {
    max: 8,
    idle_timeout: 30,
    onnotice: () => { /* silence NOTICEs */ },
  });
if (process.env.NODE_ENV !== 'production') globalThis.__mathStudySql = sql;

export default sql;
