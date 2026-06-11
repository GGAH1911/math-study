// 사용자별 개념 숙달(concept_mastery) read/write.
// 멀티유저: mastery 는 frontmatter 전역값이 아니라 (user_id, concept_id) 행이 SSOT.
// frontmatter 의 mastery 는 첫 가입 시 seed 로만 쓰이고 이후엔 동결(vestigial).
import sql from './db.ts';

export type MasteryLevel = 'unknown' | 'learning' | 'proficient' | 'mastered';
export const MASTERY_LEVELS: MasteryLevel[] = ['unknown', 'learning', 'proficient', 'mastered'];

export type MasteryRow = {
  concept_id: string;
  mastery: MasteryLevel;
  mastery_evidence: string[];
  mastery_updated: string | null;
};

export async function getMastery(userId: string, conceptId: string): Promise<MasteryRow | null> {
  const rows = await sql<MasteryRow[]>`
    SELECT concept_id, mastery, mastery_evidence, mastery_updated
    FROM concept_mastery WHERE user_id = ${userId} AND concept_id = ${conceptId} LIMIT 1
  `;
  return rows[0] ?? null;
}

// 사용자의 전체 mastery 맵 (concept_id → level). 없는 개념은 'unknown' 으로 간주.
export async function getMasteryMap(userId: string): Promise<Map<string, MasteryLevel>> {
  const rows = await sql<{ concept_id: string; mastery: MasteryLevel }[]>`
    SELECT concept_id, mastery FROM concept_mastery WHERE user_id = ${userId}
  `;
  const m = new Map<string, MasteryLevel>();
  for (const r of rows) m.set(r.concept_id, r.mastery);
  return m;
}

// 복습 도래(due) 개념 집합. concept_mastery.next_review 가 오늘(KST) 이하인 행의 concept_id.
// next_review 는 date 컬럼이라 타임존 없이 비교 — 비교 기준일도 Asia/Seoul 의 '오늘'로 맞춘다.
// (지도의 단원별 dueCount·오늘의 항로 복습 leg 가 이 집합을 소비.)
export async function getDueConceptIds(userId: string): Promise<Set<string>> {
  const rows = await sql<{ concept_id: string }[]>`
    SELECT concept_id FROM concept_mastery
     WHERE user_id = ${userId}
       AND next_review IS NOT NULL
       AND next_review <= (now() AT TIME ZONE 'Asia/Seoul')::date
  `;
  return new Set(rows.map((r) => r.concept_id));
}

// 레벨별 카운트 (대시보드 도넛용). 'unknown' 은 (총 개념수 - 기록된 수)로 보정해야
// 하므로 호출부에서 totalConcepts 를 빼서 계산. 여기선 기록된 행만 집계.
export async function getMasteryCounts(userId: string): Promise<Record<MasteryLevel, number>> {
  const rows = await sql<{ mastery: MasteryLevel; n: number }[]>`
    SELECT mastery, count(*)::int AS n FROM concept_mastery WHERE user_id = ${userId} GROUP BY mastery
  `;
  const out: Record<MasteryLevel, number> = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
  for (const r of rows) out[r.mastery] = r.n;
  return out;
}

// mastery 승급 + evidence dedupe append. 이전 레벨(from) 반환.
export async function promoteMastery(
  userId: string,
  conceptId: string,
  to: MasteryLevel,
  newEvidence: string[],
): Promise<{ from: MasteryLevel; to: MasteryLevel; evidenceCount: number }> {
  const existing = await getMastery(userId, conceptId);
  const from = existing?.mastery ?? 'unknown';
  const evidence = [...(existing?.mastery_evidence ?? [])];
  for (const e of newEvidence) if (e && !evidence.includes(e)) evidence.push(e);
  await sql`
    INSERT INTO concept_mastery (user_id, concept_id, mastery, mastery_evidence, mastery_updated)
    VALUES (${userId}, ${conceptId}, ${to}, ${sql.json(evidence)}, NOW())
    ON CONFLICT (user_id, concept_id)
      DO UPDATE SET mastery = ${to}, mastery_evidence = ${sql.json(evidence)}, mastery_updated = NOW()
  `;
  return { from, to, evidenceCount: evidence.length };
}
