// 랜덤 모의시험 조립: 공통 22 + 선택 8 을 (subject, killer_tier) 버킷에서 무작위 추출.
// 실제 수능 난이도 분포 근사 — 코퍼스엔 high tier 없으므로 early/mid/killer 로 배분.
// SSR(prerender=false)에서 호출 → Math.random 가용(매 요청 새 시험).
import type { P } from './problem-card';

export const ELECTIVES = ['미적분', '확률과통계', '기하'];

const COMMON_PLAN: Record<string, number> = { early: 6, mid: 11, killer: 5 }; // =22
const ELECTIVE_PLAN: Record<string, number> = { early: 2, mid: 4, killer: 2 }; // =8
const TIER_RANK: Record<string, number> = { early: 0, mid: 1, killer: 2 };

function pickN<T>(arr: T[], n: number): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, Math.min(n, a.length));
}

export function buildRandomExam(problems: P[], elective: string): P[] {
  const used = new Set<string>();
  const out: P[] = [];
  const fill = (subject: string, plan: Record<string, number>) => {
    for (const [tier, n] of Object.entries(plan)) {
      const avail = problems.filter(
        (p) => String(p.data.source?.subject ?? '') === subject &&
               p.data.killer_tier === tier &&
               !used.has(p.id),
      );
      for (const p of pickN(avail, n)) { out.push(p); used.add(p.id); }
    }
  };
  fill('공통', COMMON_PLAN);
  fill(elective, ELECTIVE_PLAN);
  // 공통 먼저(난이도 오름차순) → 선택(난이도 오름차순). 번호는 라우트에서 1..N 재부여.
  out.sort((a, b) => {
    const ca = a.data.source?.subject === '공통' ? 0 : 1;
    const cb = b.data.source?.subject === '공통' ? 0 : 1;
    if (ca !== cb) return ca - cb;
    return (TIER_RANK[a.data.killer_tier ?? 'mid'] ?? 1) - (TIER_RANK[b.data.killer_tier ?? 'mid'] ?? 1);
  });
  return out;
}
