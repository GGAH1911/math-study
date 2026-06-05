import { useEffect, useRef, useState } from 'react';

type Round = { name: string; status: 'ok' | 'fail' | 'pending'; detail: string };
type Proc = { pid: number; etime: string; cmd: string };
type Crop = {
  url: string; name: string; slug: string; subject: string; number: number;
  mtime: number; valid: 'ok' | 'invalid' | 'failed' | 'unknown'; reason?: string;
};
type Solcache = {
  total: number; done: number; parallel: number;
  cached: number; flagged: number; skipped: number; errored: number;
  models: Record<string, number>;
  last: { stem: string; result: string } | null;
  passPct: number | null; finished: boolean;
};
type Ingest = {
  round: string;
  pages: number; located: number; cropped: number;
  meta: { done: number; total: number };
  answers: number | null; dbUpserted: number | null;
  stage: string;
};
const INGEST_STAGE_LABEL: Record<string, string> = {
  render: '페이지 렌더링', bbox: '문항 탐지', crop: '크롭',
  meta: '메타데이터', answers: '정답 추출', done: '완료',
};
type Data = {
  now: number;
  log: { mtime: number; size: number; lines: string[]; path?: string | null };
  logs?: { name: string; mtime: number; size: number; live: boolean }[];
  procs: Proc[];
  solcache?: Solcache | null;
  ingest?: Ingest | null;
  summary: {
    stage: 'extract' | 'spoke' | 'auto' | 'auto_summary' | 'done' | 'unknown';
    startedAt: string | null;
    finishedAt: string | null;
    rounds: (Round & { pass?: string })[];
    spoke: { current: number; total: number; last: string | null };
    auto?: {
      totalRoundsAnnounced: number;
      currentRound: string | null;
      currentRoundPass: string | null;
    };
  };
  crops?: Crop[];
};

const STATUS_COLOR: Record<Round['status'], string> = {
  ok: 'text-emerald-400',
  fail: 'text-rose-400',
  pending: 'text-amber-400',
};
const STATUS_ICON: Record<Round['status'], string> = {
  ok: '✓',
  fail: '✗',
  pending: '◔',
};
const MODEL_LABEL: Record<string, string> = { h: 'Haiku', s: 'Sonnet', o: 'Opus' };

export default function ProgressView() {
  const [data, setData] = useState<Data | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [paused, setPaused] = useState(false);
  const [auto, setAuto] = useState(true);
  const [selectedLog, setSelectedLog] = useState<string | null>(null);
  const logRef = useRef<HTMLPreElement>(null);
  const lastSizeRef = useRef(0);

  useEffect(() => {
    let cancelled = false;
    let timer: number | null = null;
    const fetchOnce = async () => {
      try {
        const u = selectedLog ? `/api/progress?log=${encodeURIComponent(selectedLog)}` : '/api/progress';
        const r = await fetch(u, { cache: 'no-store' });
        const j = (await r.json()) as Data;
        if (!cancelled) {
          setData(j);
          setErr(null);
        }
      } catch (e) {
        if (!cancelled) setErr(String(e));
      }
      if (!cancelled && !paused) timer = window.setTimeout(fetchOnce, 2000);
    };
    fetchOnce();
    return () => {
      cancelled = true;
      if (timer) window.clearTimeout(timer);
    };
  }, [paused, selectedLog]);

  useEffect(() => {
    if (!data || !auto || !logRef.current) return;
    if (data.log.size === lastSizeRef.current) return;
    lastSizeRef.current = data.log.size;
    logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [data, auto]);

  if (err && !data) return <div className="text-rose-400">에러: {err}</div>;
  if (!data) return <div className="text-zinc-500">로딩 중…</div>;

  const { summary, procs, log } = data;
  const totalRounds = summary.rounds.length;
  const okRounds = summary.rounds.filter((r) => r.status === 'ok').length;
  const failRounds = summary.rounds.filter((r) => r.status === 'fail').length;
  const spokePct = summary.spoke.total > 0
    ? Math.round((summary.spoke.current / summary.spoke.total) * 100)
    : 0;

  const autoInfo = summary.auto;
  const okRoundsCount = summary.rounds.filter((r) => r.status === 'ok').length;
  const totalRoundsLabel = autoInfo?.totalRoundsAnnounced || summary.rounds.length || '?';
  let stageLabel: string;
  if (summary.stage === 'extract') stageLabel = '[1/2] 정답 vision 추출';
  else if (summary.stage === 'auto') {
    const cur = autoInfo?.currentRound ?? '?';
    const pass = autoInfo?.currentRoundPass ? ` (${autoInfo.currentRoundPass})` : '';
    stageLabel = `회차 재인제스트 ${okRoundsCount}/${totalRoundsLabel} — 진행: ${cur}${pass}`;
  } else if (summary.stage === 'auto_summary') stageLabel = '회차 모두 완료 — 요약 단계';
  else if (summary.stage === 'spoke') stageLabel = 'spoke 본문 채우기';
  else if (summary.stage === 'done') stageLabel = '완료';
  else stageLabel = '대기/시작 전';

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-6">
      {/* Log */}
      <section className="card p-0 overflow-hidden">
        <header className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-2 min-w-0">
            <select
              value={selectedLog ?? ''}
              onChange={(e) => setSelectedLog(e.target.value || null)}
              className="bg-zinc-900 border border-zinc-700 rounded text-xs font-mono text-zinc-200 px-2 py-1 max-w-[260px]"
              title="진행 로그 선택"
            >
              <option value="">🔄 자동 (최신 로그)</option>
              {(data.logs ?? []).map((l) => (
                <option key={l.name} value={l.name}>
                  {l.live ? '🟢' : '⚪'} {l.name} ({(l.size / 1024).toFixed(0)}KB)
                </option>
              ))}
            </select>
            {!selectedLog && data.log.path && (
              <span className="text-[11px] text-zinc-500 font-mono truncate">→ {data.log.path.split('/').pop()}</span>
            )}
          </div>
          <div className="flex items-center gap-3 text-xs text-zinc-500">
            <span>{log.lines.length} lines · {(log.size/1024).toFixed(1)} KB</span>
            <label className="inline-flex items-center gap-1 cursor-pointer">
              <input
                type="checkbox"
                checked={auto}
                onChange={(e) => setAuto(e.target.checked)}
                className="accent-indigo-400"
              />
              자동 스크롤
            </label>
            <button
              onClick={() => setPaused((p) => !p)}
              className={`px-2 py-0.5 rounded transition ${
                paused ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
              }`}
            >
              {paused ? '⏸ 일시정지됨' : '● 폴링 중 (2s)'}
            </button>
          </div>
        </header>
        <pre
          ref={logRef}
          className="text-[11px] leading-relaxed text-zinc-300 overflow-auto p-4 font-mono h-[70vh] bg-zinc-950"
        >
          {log.lines.map((line, i) => {
            let cls = '';
            if (line.startsWith('===')) cls = 'text-indigo-400 font-semibold';
            else if (line.includes('✓')) cls = 'text-emerald-400';
            else if (line.includes('✗')) cls = 'text-rose-400';
            else if (line.match(/^═+/)) cls = 'text-cyan-400 font-semibold';
            return (
              <div key={i} className={cls}>
                {line || ' '}
              </div>
            );
          })}
        </pre>
      </section>

      {/* Sidebar */}
      <aside className="space-y-4">
        {data.ingest && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">
              인제스트 · {data.ingest.round}
            </h3>
            <div className="text-2xl font-semibold tabular-nums">
              {data.ingest.meta.total > 0 ? (
                <>메타 {data.ingest.meta.done}<span className="text-base text-zinc-500"> / {data.ingest.meta.total}</span></>
              ) : (
                <span className="text-base text-zinc-300">{INGEST_STAGE_LABEL[data.ingest.stage] ?? data.ingest.stage}</span>
              )}
            </div>
            {data.ingest.meta.total > 0 && (
              <div className="mt-2 h-2 rounded bg-zinc-800 overflow-hidden">
                <div
                  className="h-full bg-indigo-500 transition-[width]"
                  style={{ width: `${Math.round((data.ingest.meta.done / Math.max(1, data.ingest.meta.total)) * 100)}%` }}
                />
              </div>
            )}
            {/* 파이프라인 단계 칩 — 정답 추출 단계가 명시적으로 보인다 */}
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-[11px] mt-2">
              <span className={data.ingest.pages ? 'text-emerald-400' : 'text-zinc-600'}>📄 {data.ingest.pages || '—'}p</span>
              <span className={data.ingest.located ? 'text-emerald-400' : 'text-zinc-600'}>📍 {data.ingest.located || '—'}문항</span>
              <span className={data.ingest.cropped ? 'text-emerald-400' : 'text-zinc-600'}>✂ {data.ingest.cropped || '—'}크롭</span>
              <span className={data.ingest.answers != null ? 'text-emerald-400' : 'text-zinc-600'}>✅ 정답 {data.ingest.answers ?? '—'}</span>
              <span className={data.ingest.dbUpserted != null ? 'text-emerald-400' : 'text-zinc-600'}>🗄 DB {data.ingest.dbUpserted ?? '—'}</span>
            </div>
          </section>
        )}

        {data.solcache && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">
              풀이 캐시 {data.solcache.finished ? '· 완료' : `· 병렬 ${data.solcache.parallel}`}
            </h3>
            <div className="text-2xl font-semibold tabular-nums">
              {data.solcache.done}<span className="text-base text-zinc-500"> / {data.solcache.total}</span>
              {data.solcache.passPct !== null && (
                <span className="text-sm text-emerald-400 ml-2">통과율 {data.solcache.passPct}%</span>
              )}
            </div>
            <div className="mt-2 h-2 rounded bg-zinc-800 overflow-hidden">
              <div
                className="h-full bg-emerald-500 transition-[width]"
                style={{ width: `${Math.round((data.solcache.done / Math.max(1, data.solcache.total)) * 100)}%` }}
              />
            </div>
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-[11px] mt-2">
              <span className="text-emerald-400">✓ 캐시 {data.solcache.cached}</span>
              {data.solcache.flagged > 0 && <span className="text-rose-400">⚑ 실패 {data.solcache.flagged}</span>}
              {data.solcache.skipped > 0 && <span className="text-zinc-500">skip {data.solcache.skipped}</span>}
              {data.solcache.errored > 0 && <span className="text-amber-400">err {data.solcache.errored}</span>}
            </div>
            {Object.keys(data.solcache.models).length > 0 && (
              <div className="text-[11px] text-zinc-500 mt-1">
                {['h', 's', 'o']
                  .filter((k) => data.solcache!.models[k])
                  .map((k) => `${MODEL_LABEL[k]} ${data.solcache!.models[k]}`)
                  .join(' · ')}
              </div>
            )}
            {data.solcache.last && (
              <div className="text-[11px] text-zinc-500 mt-2 truncate" title={`${data.solcache.last.stem} → ${data.solcache.last.result}`}>
                최근: {data.solcache.last.stem.replace(/^.*_/, '#')} → {data.solcache.last.result}
              </div>
            )}
          </section>
        )}

        {!data.solcache && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">단계</h3>
            <div className="text-base font-semibold">{stageLabel}</div>
            {summary.startedAt && <div className="text-xs text-zinc-500 mt-1">시작: {summary.startedAt}</div>}
            {summary.finishedAt && <div className="text-xs text-emerald-400 mt-1">완료: {summary.finishedAt}</div>}
          </section>
        )}

        {totalRounds > 0 && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">회차 ({okRounds}/{totalRounds} ✓ · {failRounds} ✗)</h3>
            <ul className="space-y-1 text-sm">
              {summary.rounds.map((r) => (
                <li key={r.name} className="flex items-center gap-2">
                  <span className={STATUS_COLOR[r.status]}>{STATUS_ICON[r.status]}</span>
                  <span className="font-medium text-zinc-200">{r.name}</span>
                  {r.detail && <span className="text-[11px] text-zinc-500 truncate" title={r.detail}>{r.detail.slice(0, 50)}</span>}
                </li>
              ))}
            </ul>
          </section>
        )}

        {summary.spoke.total > 0 && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">Spoke 채우기</h3>
            <div className="text-2xl font-semibold">
              {summary.spoke.current} <span className="text-base text-zinc-500">/ {summary.spoke.total}</span>
            </div>
            <div className="mt-2 h-2 rounded bg-zinc-800 overflow-hidden">
              <div className="h-full bg-emerald-500" style={{ width: `${spokePct}%` }} />
            </div>
            {summary.spoke.last && (
              <div className="text-[11px] text-zinc-500 mt-2 truncate" title={summary.spoke.last}>
                최근: {summary.spoke.last}
              </div>
            )}
          </section>
        )}

        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500 mb-2">살아있는 프로세스 ({procs.length})</h3>
          {procs.length === 0 ? (
            <div className="text-sm text-zinc-500">없음 (완료됐거나 시작 전)</div>
          ) : (
            <ul className="space-y-2 text-xs">
              {procs.map((p) => (
                <li key={p.pid} className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-zinc-400">PID {p.pid}</span>
                    <span className="text-zinc-500">{p.etime}</span>
                  </div>
                  <div className="text-[10px] text-zinc-600 font-mono break-all">{p.cmd}</div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </aside>

      {/* Crop preview grid — spans full width below the log + sidebar */}
      <section className="card lg:col-span-2">
        <header className="flex items-center justify-between mb-3">
          <h3 className="text-xs uppercase tracking-[0.15em] text-zinc-500">
            최근 크롭 프리뷰 {data.crops && data.crops.length > 0 ? `(${data.crops.length})` : ''}
          </h3>
          <div className="text-[10px] text-zinc-600 flex items-center gap-3">
            <span><span className="text-emerald-400">●</span> 정상</span>
            <span><span className="text-amber-400">●</span> 검증 경고</span>
            <span><span className="text-rose-400">●</span> 실패</span>
          </div>
        </header>
        {!data.crops || data.crops.length === 0 ? (
          <div className="text-sm text-zinc-500">아직 크롭된 이미지가 없습니다.</div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {data.crops.map((c) => {
              const borderCls =
                c.valid === 'ok' ? 'border-emerald-500/40' :
                c.valid === 'invalid' ? 'border-amber-500/60' :
                c.valid === 'failed' ? 'border-rose-500/60' :
                'border-zinc-700';
              const badge =
                c.valid === 'ok' ? '✓' :
                c.valid === 'invalid' ? '⚠' :
                c.valid === 'failed' ? '✗' : '?';
              const badgeCls =
                c.valid === 'ok' ? 'text-emerald-400' :
                c.valid === 'invalid' ? 'text-amber-400' :
                c.valid === 'failed' ? 'text-rose-400' : 'text-zinc-500';
              return (
                <a
                  key={c.name}
                  href={c.url}
                  target="_blank"
                  rel="noopener"
                  className={`block border ${borderCls} rounded overflow-hidden bg-zinc-900/50 hover:border-indigo-400 transition`}
                  title={c.reason ?? c.name}
                >
                  <div className="relative bg-white">
                    <img
                      src={c.url}
                      alt={c.name}
                      className="w-full h-32 object-cover object-top"
                      loading="lazy"
                    />
                    <span className={`absolute top-1 right-1 px-1.5 py-0.5 text-xs font-mono bg-zinc-900/80 rounded ${badgeCls}`}>
                      {badge}
                    </span>
                  </div>
                  <div className="px-2 py-1.5 text-[10px]">
                    <div className="font-mono text-zinc-300 truncate">{c.slug}</div>
                    <div className="text-zinc-500">{c.subject} #{c.number}</div>
                  </div>
                </a>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
