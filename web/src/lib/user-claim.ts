// 첫 실(實)가입 계정이 기존 single-user 데이터를 상속(claim)한다.
//  - problem_state / problem_attempts: legacy(SINGLE_USER_ID) → 새 유저로 user_id 재배정.
//  - concept_mastery: frontmatter 의 전역 mastery 를 새 유저 행으로 시드(전역 1인분 → 첫 유저).
// 멱등 + 경합 안전: legacy.is_legacy 플래그를 FOR UPDATE 로 잠그고, claim 후 false 로 내려
// 두 번째 가입부터는 fresh(상속 없음). legacy 행은 삭제하지 않고 비활성 유지(FK 안전).
import sql, { SINGLE_USER_ID } from './db.ts';
import { getCollection } from 'astro:content';

export async function claimLegacyDataIfFirst(
  newUserId: string,
): Promise<{ claimed: boolean; reassignedState: number; masterySeeded: number }> {
  // 빠른 경로: 이미 claim 됐으면 즉시 종료(트랜잭션·fs 로드 회피).
  const pre = await sql`SELECT 1 FROM users WHERE id = ${SINGLE_USER_ID} AND is_legacy = TRUE`;
  if (pre.length === 0) return { claimed: false, reassignedState: 0, masterySeeded: 0 };

  // 시드 소스(frontmatter)는 트랜잭션 밖에서 로드해 트랜잭션을 짧게 유지.
  const concepts = await getCollection('concepts');
  const seed = concepts
    .filter((c) => c.data.mastery && c.data.mastery !== 'unknown')
    .map((c) => ({
      id: c.id,
      mastery: c.data.mastery,
      evidence: JSON.stringify(c.data.mastery_evidence ?? []),
      updated: c.data.mastery_updated ?? null,
      review_state: c.data.review_state ?? null,
      next_review: c.data.next_review ?? null,
    }));

  return sql.begin(async (tx) => {
    // 잠금 + 재확인(경합: 다른 가입이 먼저 claim 했을 수 있음).
    const legacy = await tx`SELECT id FROM users WHERE id = ${SINGLE_USER_ID} AND is_legacy = TRUE FOR UPDATE`;
    if (legacy.length === 0) return { claimed: false, reassignedState: 0, masterySeeded: 0 };

    const st = await tx`UPDATE problem_state SET user_id = ${newUserId} WHERE user_id = ${SINGLE_USER_ID}`;
    await tx`UPDATE problem_attempts SET user_id = ${newUserId} WHERE user_id = ${SINGLE_USER_ID}`;

    for (const s of seed) {
      await tx`
        INSERT INTO concept_mastery (user_id, concept_id, mastery, mastery_evidence, mastery_updated, review_state, next_review)
        VALUES (${newUserId}, ${s.id}, ${s.mastery}, ${s.evidence}::jsonb, ${s.updated}, ${s.review_state}, ${s.next_review})
        ON CONFLICT (user_id, concept_id) DO NOTHING
      `;
    }

    // 플레이스홀더를 비활성 유지(삭제 X → FK 안전), claim 재발 방지.
    await tx`UPDATE users SET is_legacy = FALSE WHERE id = ${SINGLE_USER_ID}`;
    return { claimed: true, reassignedState: st.count ?? 0, masterySeeded: seed.length };
  });
}
