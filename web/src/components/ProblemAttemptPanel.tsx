// Student answer-entry panel on /problems/[slug].
// - GET /api/problem-state    on mount → show current state + recent attempts
// - POST /api/attempt         on submit → record + SRS update + show feedback
// - POST /api/problem-state   for "다시" / "이미 알아요" / "스킵" actions
import { useEffect, useRef, useState } from 'react';
import MathField from './MathField.tsx';
import { REVIEW_STATE_LABEL_KO } from '../lib/srs.ts';

type State = {
  status: string;
  review_state: 'new' | 'learning' | 'mature';
  next_review: string | null;
  last_attempted: string | null;
  attempt_count: number;
};
type Attempt = {
  answer_given: string | null;
  is_correct: boolean | null;
  attempted_at: string;
  time_taken_sec: number | null;
  notes: string | null;
};

const STATE_LABEL: Record<string, string> = {
  new: '🌱 신규',
  learning: '📘 학습중',
  mature: '🌳 익힘',
};

export default function ProblemAttemptPanel({ slug }: { slug: string }) {
  const [answer, setAnswer] = useState('');
  const [useMathInput, setUseMathInput] = useState(false);
  const [notes, setNotes] = useState('');
  const [notesMathOpen, setNotesMathOpen] = useState(false);
  const [notesMathLatex, setNotesMathLatex] = useState('');
  const [state, setState] = useState<State | null>(null);
  const [recent, setRecent] = useState<Attempt[]>([]);
  const [feedback, setFeedback] = useState<null | {
    correct: boolean | null; expected: string | null;
    nextReview: string; reviewState: string; intervalDays: number;
  }>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const startedAt = useRef<number>(Date.now());
  const notesRef = useRef<HTMLTextAreaElement | null>(null);

  function insertNotesMath() {
    if (!notesMathLatex.trim()) return;
    const wrapped = `$${notesMathLatex}$`;
    const ta = notesRef.current;
    if (!ta) { setNotes((p) => p + (p.endsWith(' ') ? '' : ' ') + wrapped); }
    else {
      const start = ta.selectionStart ?? notes.length;
      const end = ta.selectionEnd ?? notes.length;
      const before = notes.slice(0, start);
      const after = notes.slice(end);
      const sep = before && !before.endsWith(' ') ? ' ' : '';
      setNotes(before + sep + wrapped + after);
      setTimeout(() => {
        ta.focus();
        const pos = (before + sep + wrapped).length;
        ta.setSelectionRange(pos, pos);
      }, 0);
    }
    setNotesMathLatex('');
    setNotesMathOpen(false);
  }

  async function refresh() {
    try {
      const r = await fetch(`/api/problem-state?slug=${encodeURIComponent(slug)}`, { cache: 'no-store' });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      setState(j.state);
      setRecent(j.recentAttempts ?? []);
    } catch (e) {
      // Silent — first-time problems may legitimately have no row.
      setState(null);
      setRecent([]);
    }
  }
  useEffect(() => { refresh(); startedAt.current = Date.now(); }, [slug]);

  async function submit() {
    if (!answer.trim() || busy) return;
    setBusy(true); setErr(null);
    try {
      const r = await fetch('/api/attempt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slug,
          answer: answer.trim(),
          notes: notes.trim() || undefined,
          timeTakenSec: Math.min(36000, Math.floor((Date.now() - startedAt.current) / 1000)),
        }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error ?? `HTTP ${r.status}`);
      setFeedback({
        correct: j.correct, expected: j.expected,
        nextReview: j.nextReview, reviewState: j.reviewState, intervalDays: j.intervalDays,
      });
      setNotes('');
      await refresh();
    } catch (e) {
      setErr(String((e as Error).message ?? e));
    } finally { setBusy(false); }
  }

  async function action(kind: 'reset' | 'mark-mastered' | 'skip') {
    setBusy(true); setErr(null);
    try {
      const r = await fetch('/api/problem-state', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, action: kind }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setFeedback(null);
      setAnswer('');
      await refresh();
    } catch (e) { setErr(String((e as Error).message ?? e)); }
    finally { setBusy(false); }
  }

  return (
    <section className="card space-y-3">
      <header className="flex items-center justify-between">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)]">풀이 제출</h3>
        {state && (
          <span className="text-[11px] text-zinc-400">
            {STATE_LABEL[state.review_state] ?? state.review_state}
            {state.next_review && ` · 다음복습 ${state.next_review}`}
            {' · '}{state.attempt_count}회
          </span>
        )}
      </header>

      <div className="flex gap-2 items-start">
        <div className="flex-1 space-y-1">
          {useMathInput ? (
            <MathField
              value={answer}
              onChange={setAnswer}
              onSubmit={submit}
              placeholder="예: \\frac{1}{2} 또는 30"
              autoFocus
              rows={1}
              disabled={busy}
            />
          ) : (
            <input
              type="text"
              placeholder="정답 (예: 3 또는 ③ 또는 30)"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) submit(); }}
              disabled={busy}
              maxLength={200}
              className="w-full px-3 py-2 rounded bg-zinc-900 border border-zinc-800 focus:border-indigo-500 outline-none text-sm font-mono"
            />
          )}
          <label className="flex items-center gap-1.5 text-[10px] text-zinc-500 cursor-pointer hover:text-zinc-300">
            <input
              type="checkbox"
              checked={useMathInput}
              onChange={(e) => setUseMathInput(e.target.checked)}
              className="accent-indigo-400"
            />
            ∑ 수식 입력기 사용 (분수/적분 등)
          </label>
        </div>
        <button
          type="button"
          onClick={submit}
          disabled={busy || !answer.trim()}
          className="px-3 py-2 rounded bg-indigo-500/20 hover:bg-indigo-500/30 disabled:opacity-40 border border-indigo-500/30 text-indigo-200 text-sm transition"
        >제출</button>
      </div>

      <div className="space-y-1">
        <textarea
          ref={notesRef}
          placeholder="메모 (선택). 수식은 $ 기호로 감싸기."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          maxLength={2000}
          rows={2}
          className="w-full px-3 py-2 rounded bg-zinc-900 border border-zinc-800 focus:border-indigo-500 outline-none text-xs"
        />
        <div className="flex items-center justify-end">
          <button
            type="button"
            onClick={() => setNotesMathOpen((v) => !v)}
            className={`text-[10px] px-2 py-0.5 rounded border transition ${
              notesMathOpen
                ? 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300'
                : 'border-zinc-700 text-zinc-500 hover:text-zinc-200'
            }`}
          >∑ 메모에 수식 삽입</button>
        </div>
        {notesMathOpen && (
          <div className="rounded border border-indigo-500/30 bg-indigo-500/5 p-2 space-y-1.5">
            <MathField
              value={notesMathLatex}
              onChange={setNotesMathLatex}
              onSubmit={insertNotesMath}
              placeholder="예: \\sum_{k=1}^n k"
              autoFocus
              rows={1}
            />
            <div className="flex justify-end gap-1.5">
              <button onClick={() => { setNotesMathLatex(''); setNotesMathOpen(false); }}
                      className="text-[10px] text-zinc-500 hover:text-zinc-200 px-1.5">취소</button>
              <button onClick={insertNotesMath} disabled={!notesMathLatex.trim()}
                      className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 disabled:opacity-40">삽입</button>
            </div>
          </div>
        )}
      </div>

      {feedback && (
        <div
          className={`rounded px-3 py-2 text-sm border ${
            feedback.correct === true ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
            : feedback.correct === false ? 'bg-rose-500/10 border-rose-500/30 text-rose-300'
            : 'bg-zinc-700/40 border-zinc-700 text-zinc-300'
          }`}
        >
          {feedback.correct === true && <>✓ 정답! 다음 복습: <code>{feedback.nextReview}</code> ({feedback.intervalDays}일 후 · {REVIEW_STATE_LABEL_KO[feedback.reviewState] ?? feedback.reviewState})</>}
          {feedback.correct === false && <>✗ 오답. 정답은 <code>{feedback.expected}</code>. 내일 다시 풀어요.</>}
          {feedback.correct === null && <>기록됨 (정답 데이터 없음). 다음 복습: <code>{feedback.nextReview}</code></>}
        </div>
      )}

      {err && <div className="text-xs text-rose-400">⚠ {err}</div>}

      <div className="flex flex-wrap gap-2 pt-2 border-t border-zinc-800">
        <button onClick={() => action('mark-mastered')} disabled={busy}
                className="text-xs px-2 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/20">
          ✓ 이미 알아요
        </button>
        <button onClick={() => action('skip')} disabled={busy}
                className="text-xs px-2 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300 hover:bg-amber-500/20">
          ⏭ 1주일 미루기
        </button>
        <button onClick={() => action('reset')} disabled={busy}
                className="text-xs px-2 py-1 rounded bg-zinc-700/40 border border-zinc-700 text-zinc-300 hover:bg-zinc-700/60">
          ↺ 상태 초기화
        </button>
      </div>

      {recent.length > 0 && (
        <details className="pt-2 border-t border-zinc-800">
          <summary className="text-[11px] text-zinc-500 cursor-pointer hover:text-zinc-300">최근 {recent.length}회 시도</summary>
          <ul className="mt-2 space-y-1 text-[11px]">
            {recent.map((a, i) => (
              <li key={i} className="flex items-center gap-2 font-mono">
                <span className={
                  a.is_correct === true ? 'text-emerald-400'
                  : a.is_correct === false ? 'text-rose-400'
                  : 'text-zinc-500'
                }>
                  {a.is_correct === true ? '✓' : a.is_correct === false ? '✗' : '·'}
                </span>
                <span className="text-zinc-200">{a.answer_given ?? ''}</span>
                <span className="text-zinc-500 ml-auto">{new Date(a.attempted_at).toLocaleString('ko')}</span>
              </li>
            ))}
          </ul>
        </details>
      )}
    </section>
  );
}
