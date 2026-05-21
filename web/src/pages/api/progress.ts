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

function readTail(): { lines: string[]; mtime: number; size: number; path: string | null } {
  const path = findActiveLog();
  if (!path) return { lines: ['(no log yet)'], mtime: 0, size: 0, path: null };
  const st = statSync(path);
  const text = readFileSync(path, 'utf-8');
  const all = text.split('\n');
  const lines = all.length > MAX_LINES ? all.slice(-MAX_LINES) : all;
  return { lines, mtime: st.mtimeMs, size: st.size, path };
}

function aliveProcs(): { pid: number; etime: string; cmd: string }[] {
  try {
    const out = execSync(
      `pgrep -af "extract_all_answers|fill_spoke_bodies|post_manifest|auto_complete_rounds|ingest_round" 2>/dev/null || true`,
      { encoding: 'utf-8' },
    );
    const procs: { pid: number; etime: string; cmd: string }[] = [];
    for (const line of out.split('\n')) {
      const m = line.match(/^(\d+)\s+(.+)$/);
      if (!m) continue;
      const pid = parseInt(m[1], 10);
      const cmd = m[2];
      if (cmd.includes('pgrep') || cmd.includes('progress.ts')) continue;
      try {
        const et = execSync(`ps -p ${pid} -o etime= 2>/dev/null || echo ''`, { encoding: 'utf-8' }).trim();
        procs.push({ pid, etime: et, cmd: cmd.length > 140 ? cmd.slice(0, 140) + '…' : cmd });
      } catch { /* ignore */ }
    }
    return procs;
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
  const imagesDir = '/home/insung/Projects/math-study/web/public/problem-images';
  if (!existsSync(imagesDir)) return [];
  const validationCache: Record<string, { invalid: Set<string>; failed: Set<string>; reasons: Map<string, string> }> = {};
  const loadVal = (slug: string) => {
    if (validationCache[slug]) return validationCache[slug];
    const p = `/home/insung/Projects/math-study/db/raw/${slug}/missing.json`;
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

export const GET: APIRoute = () => {
  const { lines, mtime, size, path } = readTail();
  const procs = aliveProcs();
  const summary = parseSummary(lines);
  const crops = recentCrops(24);
  return new Response(
    JSON.stringify({
      now: Date.now(),
      log: { mtime, size, lines, path },
      procs,
      summary,
      crops,
    }),
    { status: 200, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
  );
};
