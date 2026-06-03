import { useCallback, useMemo, useRef, useState } from 'react';
import Timer from './Timer';

export type ExamProblem = {
  slug: string;
  number: number;
  subject: string;
  format: string; // choice | numeric | descriptive
  image: string;
  score: number;
};
type Props = { title: string; problems: ExamProblem[]; durationSec: number };

type Result = { correct: boolean | null; expected: string | null };

const ELECTIVES = ['미적분', '확률과통계', '기하'];
const CIRCLED = ['①', '②', '③', '④', '⑤'];

export default function ExamRunner({ title, problems, durationSec }: Props) {
  const electivesPresent = useMemo(
    () => ELECTIVES.filter((e) => problems.some((p) => p.subject === e)),
    [problems],
  );
  const [elective, setElective] = useState<string>(electivesPresent[0] ?? '');
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState<Record<string, Result>>({});
  const startRef = useRef<number>(Date.now());

  // 공통/단일 + 선택한 선택과목만 노출 (실제 시험 구성).
  const visible = useMemo(
    () => problems.filter((p) => !ELECTIVES.includes(p.subject) || p.subject === elective),
    [problems, elective],
  );

  const answeredCount = visible.filter((p) => (answers[p.slug] ?? '').trim()).length;

  const submit = useCallback(async () => {
    if (submitting || submitted) return;
    setSubmitting(true);
    const out: Record<string, Result> = {};
    await Promise.all(
      visible.map(async (p) => {
        const ans = (answers[p.slug] ?? '').trim();
        if (!ans) { out[p.slug] = { correct: null, expected: null }; return; }
        try {
          const r = await fetch('/api/attempt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slug: p.slug, answer: ans }),
          });
          const j = await r.json();
          out[p.slug] = { correct: j.correct ?? null, expected: j.expected ?? null };
        } catch {
          out[p.slug] = { correct: null, expected: null };
        }
      }),
    );
    setResults(out);
    setSubmitted(true);
    setSubmitting(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [answers, visible, submitting, submitted]);

  const correctCount = visible.filter((p) => results[p.slug]?.correct === true).length;
  const totalScore = visible.reduce((s, p) => s + (results[p.slug]?.correct === true ? p.score : 0), 0);
  const maxScore = visible.reduce((s, p) => s + p.score, 0);
  const elapsedMin = submitted ? Math.round((Date.now() - startRef.current) / 60000) : 0;

  return (
    <div className="max-w-3xl mx-auto px-4 py-5 space-y-4">
      {/* sticky 헤더 */}
      <div className="sticky top-0 z-20 -mx-4 px-4 py-2.5 bg-[color:var(--color-bg)]/95 backdrop-blur border-b border-[color:var(--color-border)] flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="text-sm font-semibold truncate">{title}</div>
          <div className="text-[11px] text-[color:var(--color-subtle)]">
            {submitted ? `채점 완료 · ${elapsedMin}분` : `${answeredCount}/${visible.length} 응답`}
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {!submitted && <Timer seconds={durationSec} onExpire={submit} />}
          {!submitted ? (
            <button
              type="button"
              onClick={submit}
              disabled={submitting}
              className="px-3 py-1.5 rounded-md bg-[color:var(--color-accent-strong)] text-white text-sm font-medium disabled:opacity-60"
            >{submitting ? '채점 중…' : '제출'}</button>
          ) : (
            <a href="/exam" className="px-3 py-1.5 rounded-md border border-[color:var(--color-border)] text-sm">다른 시험</a>
          )}
        </div>
      </div>

      {/* 선택과목 picker */}
      {!submitted && electivesPresent.length > 1 && (
        <div className="flex items-center gap-2 text-xs flex-wrap">
          <span className="text-[color:var(--color-subtle)]">선택과목</span>
          {electivesPresent.map((e) => (
            <button
              key={e}
              type="button"
              onClick={() => setElective(e)}
              className={`chip ${elective === e ? 'border-[color:var(--color-accent)] text-[color:var(--color-text)]' : 'opacity-50'}`}
            >{e}</button>
          ))}
        </div>
      )}

      {/* 점수 배너 */}
      {submitted && (
        <div className="card text-center space-y-1">
          <div className="text-3xl font-bold tabular-nums">{totalScore}<span className="text-lg text-[color:var(--color-muted)]"> / {maxScore}점</span></div>
          <div className="text-sm text-[color:var(--color-muted)]">{correctCount} / {visible.length} 정답</div>
        </div>
      )}

      {/* 문제 목록 */}
      {visible.map((p) => {
        const r = results[p.slug];
        const mine = (answers[p.slug] ?? '').trim();
        const mark = !submitted ? null : r?.correct === true ? 'ok' : r?.correct === false ? 'no' : 'skip';
        return (
          <div
            key={p.slug}
            className={`card space-y-2 ${mark === 'ok' ? 'border-emerald-500/40' : mark === 'no' ? 'border-rose-500/40' : ''}`}
          >
            <div className="flex items-center justify-between gap-2 text-sm">
              <span className="font-semibold">
                {!ELECTIVES.includes(p.subject) && p.subject !== '단일' ? `${p.subject} ` : ''}{p.number}번
                <span className="text-[color:var(--color-subtle)] font-normal text-xs"> · {p.score}점</span>
              </span>
              {mark === 'ok' && <span className="text-emerald-400 text-xs">✓ 정답</span>}
              {mark === 'no' && <span className="text-rose-400 text-xs">✗ 오답</span>}
              {mark === 'skip' && <span className="text-[color:var(--color-subtle)] text-xs">— 미응답</span>}
            </div>

            <a href={`/problems/${p.slug}`} target="_blank" rel="noopener" title="문제 페이지 새 탭">
              <img src={p.image} alt={`${p.number}번`} loading="lazy" decoding="async" className="problem-image" />
            </a>

            {/* 답안 입력 */}
            {!submitted ? (
              p.format === 'choice' ? (
                <div className="flex gap-1.5">
                  {CIRCLED.map((c, i) => {
                    const v = String(i + 1);
                    const on = mine === v;
                    return (
                      <button
                        key={v}
                        type="button"
                        onClick={() => setAnswers((a) => ({ ...a, [p.slug]: on ? '' : v }))}
                        className={`size-9 rounded-md border text-base ${on ? 'bg-[color:var(--color-accent-strong)] text-white border-transparent' : 'border-[color:var(--color-border)] text-[color:var(--color-muted)]'}`}
                      >{c}</button>
                    );
                  })}
                </div>
              ) : (
                <input
                  type="text"
                  inputMode="numeric"
                  value={mine}
                  onChange={(e) => setAnswers((a) => ({ ...a, [p.slug]: e.target.value }))}
                  placeholder="단답 (정수)"
                  className="w-32 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded-md px-3 py-1.5 text-sm focus:outline-none focus:border-[color:var(--color-accent)]"
                />
              )
            ) : (
              <div className="flex items-center gap-4 text-sm">
                <span className="text-[color:var(--color-muted)]">내 답 <b className="text-[color:var(--color-text)]">{mine || '—'}</b></span>
                {r?.expected && <span className="text-[color:var(--color-muted)]">정답 <b className="text-emerald-300">{r.expected}</b></span>}
                <a href={`/problems/${p.slug}`} className="ml-auto text-[color:var(--color-accent)] text-xs hover:underline">풀이 보기 →</a>
              </div>
            )}
          </div>
        );
      })}

      {/* 하단 제출 */}
      {!submitted && (
        <button
          type="button"
          onClick={submit}
          disabled={submitting}
          className="w-full py-2.5 rounded-md bg-[color:var(--color-accent-strong)] text-white font-medium disabled:opacity-60"
        >{submitting ? '채점 중…' : `제출하고 채점 (${answeredCount}/${visible.length})`}</button>
      )}
    </div>
  );
}
