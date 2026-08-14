import type { APIRoute } from 'astro';
import { readFileSync, statSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

export const prerender = false;

// Log candidates, newest mtime wins. /tmp/ingest_logs/extended_*.log comes
// from auto_complete_rounds.py started by the assistant; /tmp/post_manifest.log
// is the legacy single-file log used by earlier post-manifest runs.
const INGEST_LOG_DIR = '/tmp/ingest_logs';
const LEGACY_LOG_PATH = '/tmp/post_manifest.log';
const MAX_LINES = 400;

function findActiveLog(): string | null {
  const candidates: { path: string; mtime: number }[] = [];
  if (existsSync(LEGACY_LOG_PATH)) {
    try { candidates.push({ path: LEGACY_LOG_PATH, mtime: statSync(LEGACY_LOG_PATH).mtimeMs }); } catch {}
  }
  if (existsSync(INGEST_LOG_DIR)) {
    try {
      for (const name of readdirSync(INGEST_LOG_DIR)) {
        if (!name.endsWith('.log')) continue;
        const p = join(INGEST_LOG_DIR, name);
        try { candidates.push({ path: p, mtime: statSync(p).mtimeMs }); } catch {}
      }
    } catch {}
  }
  if (candidates.length === 0) return null;
  candidates.sort((a, b) => b.mtime - a.mtime);
  return candidates[0].path;
}

// 모든 진행 로그 나열 (선택 UI용). live = 최근 90초 내 갱신.
function listLogs(): { name: string; mtime: number; size: number; live: boolean }[] {
  const now = Date.now();
  const seen = new Set<string>();
  const out: { name: string; mtime: number; size: number; live: boolean }[] = [];
  const add = (p: string) => {
    if (seen.has(p)) return;
    seen.add(p);
    try {
      const st = statSync(p);
      out.push({ name: p.split('/').pop() as string, mtime: st.mtimeMs, size: st.size, live: now - st.mtimeMs < 90_000 });
    } catch { /* noop */ }
  };
  if (existsSync(LEGACY_LOG_PATH)) add(LEGACY_LOG_PATH);
  if (existsSync(INGEST_LOG_DIR)) {
    try {
      for (const name of readdirSync(INGEST_LOG_DIR)) {
        if (name.endsWith('.log')) add(join(INGEST_LOG_DIR, name));
      }
    } catch { /* noop */ }
  }
  out.sort((a, b) => b.mtime - a.mtime);
  return out;
}

// 선택한 로그(name, basename만 허용 — 경로 traversal 차단). 없으면 최신 활성 로그.
function resolveLogPath(selected?: string | null): string | null {
  if (selected) {
    const safe = selected.split('/').pop();
    if (safe && safe.endsWith('.log')) {
      const p = safe === LEGACY_LOG_PATH.split('/').pop() ? LEGACY_LOG_PATH : join(INGEST_LOG_DIR, safe);
      if (existsSync(p)) return p;
    }
  }
  return findActiveLog();
}

function readTail(selected?: string | null): { lines: string[]; mtime: number; size: number; path: string | null } {
  const path = resolveLogPath(selected);
  if (!path) return { lines: ['(no log yet)'], mtime: 0, size: 0, path: null };
  const st = statSync(path);
  const text = readFileSync(path, 'utf-8');
  const all = text.split('\n');
  const lines = all.length > MAX_LINES ? all.slice(-MAX_LINES) : all;
  return { lines, mtime: st.mtimeMs, size: st.size, path };
}

// 실행 중인 스크립트 → 사람이 읽는 잡 이름. cmd 인자(도메인 등)도 살짝 덧붙인다.
function procName(cmd: string): string {
  const map: [RegExp, string][] = [
    [/gen_concept_figures/, '개념 도식 생성'],
    [/qa_concept_figures/, '개념 도식 QA'],
    [/build_solution_cache/, '풀이 캐시 빌드'],
    [/ingest_auto/, '인제스트(자동분류)'],
    [/ingest_v2/, '인제스트 v2'],
    [/ingest_ganah/, '인제스트(가나다)'],
    [/ingest_gyo12/, '인제스트(고1·2)'],
    [/fill_spoke_bodies/, '개념 본문 채우기'],
    [/regenerate|refine_opus/, '본문 재생성'],
    [/auto_complete_rounds/, '회차 일괄 인제스트'],
    [/extract_all_answers/, '정답 추출'],
  ];
  for (const [re, name] of map) if (re.test(cmd)) {
    const dom = cmd.match(/--domain\s+(\S+)/);
    return dom ? `${name} · ${dom[1]}` : name;
  }
  const m = cmd.match(/scripts\/(?:[a-z0-9_]+\/)*([a-z0-9_]+)\.(?:py|mjs)/);
  return m ? m[1] : '작업';
}

function aliveProcs(): { pid: number; etime: string; cmd: string; name: string }[] {
  try {
    // 제네릭: scripts/<...>/<name>.{py,mjs} 를 실행하는 모든 잡 자동 감지(파이썬 인제스트·캐시빌드 +
    // node .mjs 도식 생성/QA(gen_concept_figures·qa_concept_figures)) + 레거시 비-scripts 잡.
    const out = execSync(
      `pgrep -af "scripts/[a-z0-9_/]+\\.(py|mjs)|auto_complete_rounds|fill_spoke_bodies|extract_all_answers|post_manifest" 2>/dev/null || true`,
      { encoding: 'utf-8' },
    );
    const procs: { pid: number; etime: string; cmd: string; name: string }[] = [];
    for (const line of out.split('\n')) {
      const m = line.match(/^(\d+)\s+(.+)$/);
      if (!m) continue;
      const pid = parseInt(m[1], 10);
      const cmd = m[2];
      if (cmd.includes('pgrep') || cmd.includes('progress.ts')) continue;
      // 셸 래퍼(타이밍/리다이렉트 포함) 제외 — 실제 인터프리터(node/python) 프로세스만 표시.
      if (/\bdate \+%s\b/.test(cmd) || /^\S*\/?(?:ba|z|d|c)?sh\b/.test(cmd)) continue;
      try {
        const et = execSync(`ps -p ${pid} -o etime= 2>/dev/null || echo ''`, { encoding: 'utf-8' }).trim();
        procs.push({ pid, etime: et, name: procName(cmd), cmd: cmd.length > 140 ? cmd.slice(0, 140) + '…' : cmd });
      } catch { /* ignore */ }
    }
    return procs;
  } catch {
    return [];
  }
}

// 최근 생성된 개념 도식 — concept-figures.json 의 figure 있는 항목을 삽입 역순(최신 우선)으로.
// 라이브 gen 은 신규 figure 를 끝에 append 하므로 마지막 N 개 ≈ 가장 최근.
function recentFigures(limit = 12): Array<{ id: string; label: string; model?: string; figure: unknown }> {
  try {
    const p = join(process.cwd(), 'src', 'data', 'concept-figures.json');
    if (!existsSync(p)) return [];
    const data = JSON.parse(readFileSync(p, 'utf-8'));
    const figs = data.figures ?? {};
    const out: Array<{ id: string; label: string; model?: string; figure: unknown }> = [];
    for (const [id, v] of Object.entries(figs) as [string, any][]) {
      if (v && v.figure) out.push({ id, label: v.label ?? id, model: v.model, figure: v.figure });
    }
    return out.slice(-limit).reverse();
  } catch {
    return [];
  }
}

type Stage =
  | 'extract'        // old chain stage 1
  | 'spoke'          // old chain stage 2 OR new orchestrator final
  | 'auto'           // new orchestrator: re-ingest rounds
  | 'auto_summary'   // new orchestrator: after rounds, before fill_spoke
  | 'done'
  | 'unknown';

function parseSummary(lines: string[]) {
  const rounds: { name: string; status: 'ok' | 'fail' | 'pending'; detail: string; pass?: string }[] = [];
  let currentRound: string | null = null;
  let spokeCurrent = 0;
  let spokeTotal = 0;
  let spokeLast: string | null = null;
  let stage: Stage = 'unknown';
  let startedAt: string | null = null;
  let finishedAt: string | null = null;
  let totalRoundsAnnounced = 0;

  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith('=== START')) startedAt = line.replace('=== START', '').replace('===', '').trim();
    if (line.match(/=== auto_complete_rounds (CHAIN )?START/)) {
      stage = 'auto';
      const m = line.match(/START\s+(.+?)\s*===/);
      if (m) startedAt = m[1];
    }
    if (line.startsWith('=== DONE')) { finishedAt = line.replace('=== DONE', '').replace('===', '').trim(); stage = 'done'; }
    if (line.includes('[1/2] extract_all_answers')) stage = 'extract';
    if (line.includes('[2/2] fill_spoke_bodies')) stage = 'spoke';
    if (line.includes('[final] fill_spoke_bodies')) stage = 'spoke';
    if (line.match(/^═+\s*Summary\s*═+$/i)) stage = 'auto_summary';

    const totMatch = line.match(/Rounds to process:\s*(\d+)/);
    if (totMatch) totalRoundsAnnounced = parseInt(totMatch[1], 10);

    const roundMatch = line.match(/^═+\s*(\S+)\s*═+$/);
    if (roundMatch && roundMatch[1] !== 'Summary') {
      const name = roundMatch[1];
      // Avoid duplicate entries when ingest_round prints its own ══════ name (모의평가, 6월) ══════
      if (rounds.find((x) => x.name === name)) {
        currentRound = name;
      } else {
        currentRound = name;
        rounds.push({ name, status: 'pending', detail: '' });
      }
    }
    // Track current pass for the active round
    if (currentRound) {
      const passMatch = line.match(/\[(initial|self-fix #\d+)\]/);
      if (passMatch) {
        const r = rounds.find((x) => x.name === currentRound);
        if (r) r.pass = passMatch[1];
      }
      // Final completion line: `✓ <name> 완료 (N/M ...)` — only mark ok here
      const okFinal = line.match(/^✓\s+(\S+)\s+(최종|완료)\s+(.+)$/);
      if (okFinal && okFinal[1] === currentRound) {
        const r = rounds.find((x) => x.name === currentRound);
        if (r) { r.status = 'ok'; r.detail = okFinal[3]; }
      }
      const failFinal = line.match(/^✗\s+(\S+)\s+(최종|완료)\s+(.+)$/);
      if (failFinal && failFinal[1] === currentRound) {
        const r = rounds.find((x) => x.name === currentRound);
        if (r) { r.status = 'fail'; r.detail = failFinal[3]; }
      }
    }
    const spokeMatch = line.match(/\[\s*(\d+)\/(\d+)\]\s+([✓✗-])\s+(\S+)/);
    if (spokeMatch) {
      spokeCurrent = parseInt(spokeMatch[1], 10);
      spokeTotal = parseInt(spokeMatch[2], 10);
      spokeLast = `${spokeMatch[3]} ${spokeMatch[4]}`;
    }
    const tgtMatch = line.match(/Targets:\s*(\d+)\s+spokes/);
    if (tgtMatch) spokeTotal = parseInt(tgtMatch[1], 10);
  }

  // If we are in 'auto' stage and current round has no detail yet, surface its pass label
  const currentRoundObj = currentRound ? rounds.find((x) => x.name === currentRound) : null;
  const currentRoundPass = currentRoundObj?.pass ?? null;

  return {
    stage,
    startedAt,
    finishedAt,
    rounds,
    spoke: { current: spokeCurrent, total: spokeTotal, last: spokeLast },
    auto: {
      totalRoundsAnnounced,
      currentRound,
      currentRoundPass,
    },
  };
}

// Recent crops: surface the most-recently-cropped problem PNGs so the
// /progress page can show live previews. Each image links to its problem
// page and carries the validation status from db/raw/{slug}/missing.json.
function recentCrops(limit = 24): Array<{
  url: string; name: string; slug: string; subject: string; number: number;
  mtime: number; valid: 'ok' | 'invalid' | 'failed' | 'unknown'; reason?: string;
}> {
  // cwd = 실행 중인 dev 서버의 web 디렉토리 → 메인 리포든 git worktree든 자동 대응.
  // ★`public` 이 아니라 `private` — 기출 이미지는 인증 게이팅 때문에 정적 서빙 밖에 있다
  //   (`lib/media-root.ts`). 옛 경로면 existsSync 가 false 라 **빈 목록**을 조용히 돌려준다.
  const imagesDir = join(process.cwd(), 'private', 'problem-images');
  if (!existsSync(imagesDir)) return [];
  const validationCache: Record<string, { invalid: Set<string>; failed: Set<string>; reasons: Map<string, string> }> = {};
  const loadVal = (slug: string) => {
    if (validationCache[slug]) return validationCache[slug];
    const p = join(process.cwd(), '..', 'db', 'raw', slug, 'missing.json');
    const v = { invalid: new Set<string>(), failed: new Set<string>(), reasons: new Map<string, string>() };
    if (existsSync(p)) {
      try {
        const data = JSON.parse(readFileSync(p, 'utf-8'));
        for (const w of (data.crop_validation_warnings ?? [])) {
          const k = `${w.subject}_${String(w.number).padStart(2, '0')}`;
          v.invalid.add(k);
          if (w.reason) v.reasons.set(k, w.reason);
        }
        for (const f of (data.failed_crops ?? [])) {
          const k = `${f.subject}_${String(f.number).padStart(2, '0')}`;
          v.failed.add(k);
          if (f.reason) v.reasons.set(k, f.reason);
        }
      } catch { /* noop */ }
    }
    validationCache[slug] = v;
    return v;
  };

  let files: Array<{ name: string; mtime: number }> = [];
  try {
    for (const name of readdirSync(imagesDir)) {
      if (!name.endsWith('.png')) continue;
      try {
        const st = statSync(`${imagesDir}/${name}`);
        files.push({ name, mtime: st.mtimeMs });
      } catch { /* noop */ }
    }
  } catch { return []; }
  files.sort((a, b) => b.mtime - a.mtime);
  files = files.slice(0, limit);

  return files.map((f) => {
    // name: 2026_고1_3월모의고사_단일_05.png
    const stem = f.name.replace(/\.png$/, '');
    // last two segments are subject + number; everything before is slug
    const parts = stem.split('_');
    const number = parseInt(parts[parts.length - 1], 10);
    const subject = parts[parts.length - 2];
    const slug = parts.slice(0, -2).join('_');
    const key = `${subject}_${String(number).padStart(2, '0')}`;
    const v = loadVal(slug);
    const valid: 'ok' | 'invalid' | 'failed' | 'unknown' =
      v.failed.has(key) ? 'failed' :
      v.invalid.has(key) ? 'invalid' :
      'ok';
    return {
      url: `/problem-images/${encodeURIComponent(f.name)}`,
      name: f.name,
      slug,
      subject,
      number,
      mtime: f.mtime,
      valid,
      reason: v.reasons.get(key),
    };
  });
}

// build_solution_cache.py 진행 파싱. 로그 포맷:
//   대상 30문제 · 병렬 4 · 난이도순
//   [3/30] 2028_예시_단일_07  →  CACHED@h        (또는 FLAG(...)/skip-cached/ERROR:..)
//   통과율: 23/30 = 76%   (요약 단계)
// 인제스트 로그면 '대상 N문제'가 없어 null 반환 → 패널 숨김.
function parseSolcache(lines: string[]) {
  let total = 0, done = 0, parallel = 0;
  let cached = 0, flagged = 0, skipped = 0, errored = 0;
  const models: Record<string, number> = {};
  let last: { stem: string; result: string } | null = null;
  let passPct: number | null = null;
  let finished = false;
  for (const raw of lines) {
    const line = raw.trim();
    const head = line.match(/대상\s*(\d+)\s*문제\s*·\s*병렬\s*(\d+)/);
    if (head) { total = parseInt(head[1], 10); parallel = parseInt(head[2], 10); }
    const prog = line.match(/^\[(\d+)\/(\d+)\]\s+(\S+)\s+→\s+(.+)$/);
    if (prog) {
      done = parseInt(prog[1], 10);
      total = parseInt(prog[2], 10);
      const result = prog[4].trim();
      last = { stem: prog[3], result };
      if (result.startsWith('CACHED')) {
        cached++;
        const m = result.match(/^CACHED@(\w)/);
        if (m) models[m[1]] = (models[m[1]] ?? 0) + 1;
      } else if (result.startsWith('skip')) skipped++;
      else if (result.startsWith('ERROR')) errored++;
      else flagged++;
    }
    const pr = line.match(/통과율:\s*\d+\/\d+\s*=\s*(\d+)%/);
    if (pr) { passPct = parseInt(pr[1], 10); finished = true; }
  }
  if (total === 0) return null;
  return { total, done, parallel, cached, flagged, skipped, errored, models, last, passPct, finished };
}

// ingest_v2.py 진행 파싱. 로그 포맷:
//   ══════ 2027_6월모평 (모의평가, 6월) ══════
//     ✓ 20 pages rendered
//     ✓ 46 problems located via PDF text-layer
//     ✓ 46 problem PNGs cropped (7s)
//     [meta  N/46] ✓ # N ...
//     ✓ answers: textlayer 좌표파싱 (46 entries)   ← 정답 추출 단계
//     ✓ DB upsert 46 problems
// 라운드 마커(slug + (type, session))가 없으면 인제스트 로그가 아님 → null(패널 숨김).
function parseIngest(lines: string[]) {
  let round: string | null = null;
  let pages = 0, located = 0, cropped = 0, metaDone = 0, metaTotal = 0;
  let answers: number | null = null, dbUpserted: number | null = null;
  let stage = 'render';
  for (const raw of lines) {
    const line = raw.trim();
    let m: RegExpMatchArray | null;
    if ((m = line.match(/^═+\s*(\S+)\s*\(.+\)\s*═+$/))) {
      round = m[1]; stage = 'render';
      pages = located = cropped = metaDone = metaTotal = 0; answers = dbUpserted = null;
    }
    if ((m = line.match(/(\d+)\s*pages rendered/))) { pages = parseInt(m[1], 10); stage = 'bbox'; }
    if ((m = line.match(/(\d+)\s*problems located/))) { located = parseInt(m[1], 10); stage = 'crop'; }
    if ((m = line.match(/(\d+)\s*problem PNGs cropped/))) { cropped = parseInt(m[1], 10); stage = 'meta'; }
    if ((m = line.match(/^\[meta\s+(\d+)\/(\d+)\]/))) { metaDone = parseInt(m[1], 10); metaTotal = parseInt(m[2], 10); stage = 'meta'; }
    if ((m = line.match(/✓\s*answers:.*?(\d+)\s*entries/))) { answers = parseInt(m[1], 10); stage = 'answers'; }
    if ((m = line.match(/✓\s*DB upsert\s+(\d+)\s*problems/))) { dbUpserted = parseInt(m[1], 10); stage = 'done'; }
  }
  if (!round) return null;
  return { round, pages, located, cropped, meta: { done: metaDone, total: metaTotal }, answers, dbUpserted, stage };
}

export const GET: APIRoute = ({ url }) => {
  const selected = url.searchParams.get('log');
  const { lines, mtime, size, path } = readTail(selected);
  const procs = aliveProcs();
  const summary = parseSummary(lines);
  const solcache = parseSolcache(lines);
  const ingest = parseIngest(lines);
  const crops = recentCrops(24);
  const figures = recentFigures(12);
  const logs = listLogs();
  return new Response(
    JSON.stringify({
      now: Date.now(),
      log: { mtime, size, lines, path },
      logs,
      procs,
      summary,
      solcache,
      ingest,
      crops,
      figures,
    }),
    { status: 200, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
  );
};
