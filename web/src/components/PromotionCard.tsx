// LLM이 채팅에서 ```promote {"to":"learning","reason":"..."}``` fence를
// emit하면 이 카드가 mount되어 사용자에게 mastery 승급 승인 UI를 제공한다.
// 승인 시 /api/mastery-promote 호출 → docs/concepts/<slug>.md frontmatter 갱신.
//
// 강등도 같은 컴포넌트로 처리 (to가 현재보다 낮은 단계).

import { useState } from 'react';

export type MasteryLevel = 'unknown' | 'learning' | 'proficient' | 'mastered';

interface Props {
  slug: string;                 // 채팅 페이지의 concept slug
  to: MasteryLevel;             // LLM이 제안한 새 mastery
  reason?: string;              // LLM의 판단 근거
  evidence?: string[];          // 선택: 추가 증거 (problem md path 등)
}

const LEVELS: MasteryLevel[] = ['unknown', 'learning', 'proficient', 'mastered'];
const LEVEL_LABEL: Record<MasteryLevel, string> = {
  unknown: '아직',
  learning: '학습 중',
  proficient: '잘 앎',
  mastered: '숙달',
};
const LEVEL_COLOR: Record<MasteryLevel, string> = {
  unknown: 'bg-zinc-500/20 text-zinc-300 border-zinc-600',
  learning: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
  proficient: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
  mastered: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
};

// 적용된 제안을 localStorage 에 영속화 → 리로드/재방문 시 같은 promote 펜스가
// 다시 "적용" 버튼으로 뜨는 루프를 막는다(적용 상태가 컴포넌트 로컬 state 라 소실되던 버그).
const APPLIED_KEY = 'math-study:mastery-applied';
function loadApplied(): Set<string> {
  if (typeof window === 'undefined') return new Set();
  try { return new Set(JSON.parse(window.localStorage.getItem(APPLIED_KEY) || '[]') as string[]); } catch { return new Set(); }
}
function markApplied(key: string): void {
  if (typeof window === 'undefined') return;
  try {
    const s = loadApplied(); s.add(key);
    window.localStorage.setItem(APPLIED_KEY, JSON.stringify([...s].slice(-300)));
  } catch { /* quota/disabled */ }
}

export default function PromotionCard({ slug, to, reason, evidence }: Props) {
  const sugKey = `${slug}|${to}|${reason ?? ''}`;
  const [status, setStatus] = useState<'pending' | 'applying' | 'applied' | 'declined' | 'error'>(
    () => (loadApplied().has(sugKey) ? 'applied' : 'pending'),
  );
  const [from, setFrom] = useState<MasteryLevel | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isPromote = (toLevel: MasteryLevel) => {
    if (!from) return true;
    return LEVELS.indexOf(toLevel) > LEVELS.indexOf(from);
  };

  const apply = async () => {
    setStatus('applying');
    setError(null);
    try {
      const res = await fetch('/api/mastery-promote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, to, reason, evidence }),
      });
      const json = await res.json() as { ok?: boolean; from?: MasteryLevel; error?: string };
      if (!res.ok || !json.ok) {
        setStatus('error');
        setError(json.error ?? `HTTP ${res.status}`);
        return;
      }
      if (json.from) setFrom(json.from);
      markApplied(sugKey);
      setStatus('applied');
      // 리로드 대신 사이드바 mastery 칩을 in-place 갱신. 리로드하면 대화에 남은
      // ```promote``` 펜스가 새 카드(pending)로 다시 떠 "적용"을 반복 요구하는 루프 발생.
      window.dispatchEvent(new CustomEvent('math-study:mastery-applied', { detail: { slug, to } }));
    } catch (e) {
      setStatus('error');
      setError((e as Error).message);
    }
  };

  const decline = () => setStatus('declined');

  const verb = from ? (isPromote(to) ? '승급' : '강등') : '갱신';
  const icon = from ? (isPromote(to) ? '🎓' : '⬇') : '✦';

  return (
    <div className="my-2 rounded-lg border border-indigo-500/40 bg-indigo-500/5 p-3 text-xs">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-base">{icon}</span>
        <span className="font-semibold text-indigo-200">
          LLM 튜터의 {verb} 제안
        </span>
        <span className="ml-auto text-[10px] text-zinc-500 truncate" title={slug}>{slug}</span>
      </div>

      <div className="flex items-center gap-2 mb-2">
        {from && (
          <>
            <span className={`px-2 py-0.5 rounded border ${LEVEL_COLOR[from]}`}>
              {from} · {LEVEL_LABEL[from]}
            </span>
            <span className="text-zinc-500">→</span>
          </>
        )}
        <span className={`px-2 py-0.5 rounded border ${LEVEL_COLOR[to]}`}>
          {to} · {LEVEL_LABEL[to]}
        </span>
      </div>

      {reason && (
        <p className="text-zinc-300 mb-2 leading-relaxed">
          <span className="text-zinc-500">근거:</span> {reason}
        </p>
      )}

      {evidence && evidence.length > 0 && (
        <ul className="text-[11px] text-zinc-400 mb-2 list-disc pl-5 space-y-0.5">
          {evidence.map((e, i) => (<li key={i}>{e}</li>))}
        </ul>
      )}

      {status === 'pending' && (
        <div className="flex gap-2 mt-2">
          <button
            onClick={apply}
            className="px-3 py-1 rounded bg-indigo-500/30 border border-indigo-500/50 text-indigo-100 hover:bg-indigo-500/50 transition"
          >
            ✓ 적용
          </button>
          <button
            onClick={decline}
            className="px-3 py-1 rounded border border-zinc-700 text-zinc-400 hover:bg-zinc-800 transition"
          >
            건너뛰기
          </button>
        </div>
      )}

      {status === 'applying' && (
        <p className="text-zinc-400 text-[11px]">⏳ 적용 중…</p>
      )}

      {status === 'applied' && (
        <p className="text-emerald-300 text-[11px]">✓ 적용됨</p>
      )}

      {status === 'declined' && (
        <p className="text-zinc-500 text-[11px]">건너뜀</p>
      )}

      {status === 'error' && (
        <p className="text-rose-400 text-[11px]">⚠ {error}</p>
      )}
    </div>
  );
}
