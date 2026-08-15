// 내 정보 — 학습 현황(숙달 집계) + 튜터가 감지한 약점 패턴. 데이터는 `/api/account`.
//
// ★계정 정보와 **회원 탈퇴 흐름은 페이지에 서버 렌더로 남긴다.** 탈퇴는 파괴적 동작이고
//   인라인 스크립트가 비번 재확인·확인 문구·API 호출을 엮고 있다 — 표시 부분을 옮기자고
//   그 흐름을 다시 쓰는 건 위험 대비 이득이 없다. `hasPassword` 도 그래서 페이지에 남는다.
import { useEffect } from 'react';
import { useJsonOnce } from '../lib/content-entry.ts';

type Data = {
  counts: Record<'unknown' | 'learning' | 'proficient' | 'mastered', number>;
  recorded: number;
  profile: { weakness_patterns: string[] } | null;
};

const CHIPS = [
  { label: '마스터', v: 'mastered' },
  { label: '능숙', v: 'proficient' },
  { label: '학습중', v: 'learning' },
  { label: '미착수', v: 'unknown' },
] as const;

export function AccountMastery() {
  const s = useJsonOnce<Data>('/api/account');
  if (s.status !== 'ready') {
    return <p className="text-xs text-[color:var(--color-muted)]">불러오는 중…</p>;
  }
  const { counts, recorded } = s.data;
  return (
    <>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {CHIPS.map((c) => (
          <div className="rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-bg)] px-3 py-2.5" key={c.v}>
            <div className="flex items-center gap-1.5 text-xs text-[color:var(--color-muted)]">
              <span className={`inline-block size-1.5 rounded-full bg-[color:var(--color-mastery-${c.v})]`} />
              {c.label}
            </div>
            <div className="stat-num text-xl mt-0.5">{counts[c.v]}</div>
          </div>
        ))}
      </div>
      {recorded === 0 && (
        <p className="text-xs text-[color:var(--color-muted)] mt-3">아직 숙달 기록이 없습니다. 단원을 학습하면 여기에 쌓입니다.</p>
      )}
    </>
  );
}

export function AccountWeakness() {
  const s = useJsonOnce<Data>('/api/account');
  if (s.status !== 'ready') {
    return <p className="text-xs text-[color:var(--color-muted)]">불러오는 중…</p>;
  }
  const w = s.data.profile?.weakness_patterns ?? [];
  if (w.length === 0) {
    return <p className="text-xs text-[color:var(--color-muted)]">아직 없습니다 — 튜터와 대화하면서 막히는 지점이 자동으로 기록됩니다.</p>;
  }
  return (
    <ul className="flex flex-wrap gap-2">
      {w.map((x) => (
        <li className="px-2.5 py-1 rounded-full bg-[color:var(--color-bg)] border border-[color:var(--color-border)] text-xs text-[color:var(--color-muted)]" key={x}>{x}</li>
      ))}
    </ul>
  );
}

/**
 * 학습자 프로필 폼의 **초기값만** 채운다.
 *
 * ★폼 자체와 저장 스크립트(`#profile-form`)는 페이지에 그대로 둔다. 값만 넣으면 되는데
 *   폼을 통째로 React 로 옮기면 저장 흐름까지 다시 써야 한다 — 이득 없이 위험만 는다.
 * ★사용자가 이미 타이핑을 시작했으면 덮어쓰지 않는다(늦게 도착한 응답이 입력을 지우면 안 된다).
 */
export function AccountProfileFill() {
  const s = useJsonOnce<Data & { profile: Record<string, string | null> | null }>('/api/account');
  useEffect(() => {
    if (s.status !== 'ready' || !s.data.profile) return;
    const p = s.data.profile;
    for (const k of ['self_reported_level', 'goals', 'learning_pace', 'notes']) {
      const el = document.getElementById(k) as HTMLInputElement | HTMLTextAreaElement | null;
      if (el && !el.value) el.value = String(p[k] ?? '');
    }
  }, [s]);
  return null;
}
