// 학습자 모델 — 정량(개념 숙달 기반 자동 도출) + 정성(튜터가 누적 갱신) 프로필.
// 튜터 프롬프트에 주입해 "특정 학년 하드코딩" 대신 이 학생의 실제 수준에 맞춘다.
import sql from './db.ts';
import { getMasteryCounts } from './mastery.ts';
import { readConceptGraph } from './health.ts';

export type UserProfile = {
  self_reported_level: string | null;
  goals: string | null;
  weakness_patterns: string[];
  learning_pace: string | null;
  notes: string | null;
};

export async function getUserProfile(userId: string): Promise<UserProfile | null> {
  const rows = await sql<UserProfile[]>`
    SELECT self_reported_level, goals, weakness_patterns, learning_pace, notes
    FROM user_profile WHERE user_id = ${userId} LIMIT 1
  `;
  return rows[0] ?? null;
}

export type ProfilePatch = {
  self_reported_level?: string | null;
  goals?: string | null;
  learning_pace?: string | null;
  notes?: string | null;
  addWeaknesses?: string[]; // 약점 패턴 dedupe append
};

export async function upsertUserProfile(userId: string, patch: ProfilePatch): Promise<UserProfile> {
  const existing = await getUserProfile(userId);
  const weakness = [...(existing?.weakness_patterns ?? [])];
  for (const w of patch.addWeaknesses ?? []) if (w && !weakness.includes(w)) weakness.push(w);
  const merged: UserProfile = {
    self_reported_level: patch.self_reported_level !== undefined ? patch.self_reported_level : (existing?.self_reported_level ?? null),
    goals: patch.goals !== undefined ? patch.goals : (existing?.goals ?? null),
    learning_pace: patch.learning_pace !== undefined ? patch.learning_pace : (existing?.learning_pace ?? null),
    notes: patch.notes !== undefined ? patch.notes : (existing?.notes ?? null),
    weakness_patterns: weakness,
  };
  await sql`
    INSERT INTO user_profile (user_id, self_reported_level, goals, weakness_patterns, learning_pace, notes, updated_at)
    VALUES (${userId}, ${merged.self_reported_level}, ${merged.goals}, ${JSON.stringify(merged.weakness_patterns)}::jsonb, ${merged.learning_pace}, ${merged.notes}, NOW())
    ON CONFLICT (user_id) DO UPDATE SET
      self_reported_level = ${merged.self_reported_level}, goals = ${merged.goals},
      weakness_patterns = ${JSON.stringify(merged.weakness_patterns)}::jsonb,
      learning_pace = ${merged.learning_pace}, notes = ${merged.notes}, updated_at = NOW()
  `;
  return merged;
}

const GRADE_RANK: Record<string, number> = {
  중1: 1, 중2: 2, 중3: 3, 고1: 4, 수학1: 5, 수학2: 6, 미적분: 7, 기하: 7, 확률과통계: 7,
};
const leafOf = (id: string) => (id.split('/').pop() ?? id).replace(/_/g, ' ');

// 튜터 프롬프트에 주입할 이 학생의 학습자 컨텍스트 문자열.
export async function buildLearnerContext(userId: string): Promise<string> {
  const counts = await getMasteryCounts(userId);
  const strong = await sql<{ concept_id: string }[]>`
    SELECT concept_id FROM concept_mastery WHERE user_id = ${userId} AND mastery IN ('proficient', 'mastered')
    ORDER BY mastery_updated DESC NULLS LAST LIMIT 200
  `;
  // frontier 학년: 능숙+ 개념들이 도달한 최고 학년대.
  const graph = readConceptGraph();
  const gradeById = new Map<string, string | undefined>(graph.nodes.map((n) => [n.id, n.grade]));
  let frontier: string | null = null;
  let frontierRank = 0;
  for (const r of strong) {
    const g = gradeById.get(r.concept_id);
    const rank = g ? (GRADE_RANK[g] ?? 0) : 0;
    if (rank > frontierRank) { frontierRank = rank; frontier = g ?? null; }
  }
  const recentStrong = strong.slice(0, 6).map((r) => leafOf(r.concept_id));

  const profile = await getUserProfile(userId);
  const lines: string[] = ['--- 이 학생의 학습자 모델 (특정 학년으로 고정 가정 말고 이 데이터로 깊이 조절) ---'];

  // 정량
  const recorded = counts.learning + counts.proficient + counts.mastered;
  if (recorded === 0) {
    lines.push('정량: 아직 숙달 기록 없음(신규/초기). 기본은 기초부터, 대화로 수준 파악.');
  } else {
    lines.push(`정량(개념 숙달): 숙달 ${counts.mastered} · 능숙 ${counts.proficient} · 학습중 ${counts.learning}` +
      (frontier ? ` · 도달 학년대(능숙+ 최고) ≈ ${frontier}` : ''));
    if (recentStrong.length) lines.push(`최근 능숙+ 개념: ${recentStrong.join(', ')}`);
  }

  // 정성
  if (profile && (profile.self_reported_level || profile.goals || profile.weakness_patterns.length || profile.learning_pace)) {
    if (profile.self_reported_level) lines.push(`자기보고 수준: ${profile.self_reported_level}`);
    if (profile.goals) lines.push(`학습 목표: ${profile.goals}`);
    if (profile.weakness_patterns.length) lines.push(`약점 패턴: ${profile.weakness_patterns.slice(0, 6).join('; ')}`);
    if (profile.learning_pace) lines.push(`학습 페이스: ${profile.learning_pace}`);
  } else {
    lines.push('정성 프로필: 아직 파악된 것 없음 — 대화에서 목표·약점·페이스를 파악.');
  }

  return lines.join('\n');
}
