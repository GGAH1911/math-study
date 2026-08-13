#!/usr/bin/env node
// Nous Portal 모델 가용성 프로브 — 후보 모델에 최소 요청을 던져 성공/실패·지연을 기록한다.
//   측정 중 qwen3.7-flash 가 503(temporarily unavailable)을 간헐적으로 뱉었는데, 그게 일시적인지
//   상시적인지에 따라 모델 선택이 갈린다(캐싱 되고 판독 9.9 인데 월 $0.12 — 가용성만 되면 유력 후보).
//   한 번의 실패로 판단하지 말고 시계열로 본다.
//
// 사용:
//   node web/scripts/model_probe.mjs            # 1회 프로브(크론이 이걸 부른다)
//   node web/scripts/model_probe.mjs --report   # 누적 집계 출력
import { appendFileSync, readFileSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const MON = `${REPO}/.llm-monitor`;
if (!existsSync(MON)) mkdirSync(MON, { recursive: true });
const LOG = `${MON}/probe.jsonl`;
const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';

const MODELS = (process.env.PROBE_MODELS || [
  'qwen/qwen3.7-flash',
  'google/gemma-4-31b-it',
  '~deepseek/deepseek-v4-flash-latest',
  '~anthropic/claude-haiku-latest',
].join(',')).split(',').map((s) => s.trim()).filter(Boolean);

function report() {
  if (!existsSync(LOG)) { console.log('아직 기록 없음'); return; }
  const rows = readFileSync(LOG, 'utf8').trim().split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  if (!rows.length) { console.log('아직 기록 없음'); return; }
  const span = (rows[rows.length - 1].t - rows[0].t) / 3600000;
  console.log(`관측 ${rows.length}건 · ${span.toFixed(1)}시간\n`);
  console.log('모델'.padEnd(36) + '가용률   시도   실패   평균지연   최근실패');
  const by = {};
  for (const r of rows) { (by[r.model] ??= []).push(r); }
  for (const [m, rs] of Object.entries(by)) {
    const ok = rs.filter((r) => r.ok);
    const bad = rs.filter((r) => !r.ok);
    const lat = ok.length ? Math.round(ok.reduce((s, r) => s + r.ms, 0) / ok.length) : 0;
    const last = bad.length ? new Date(bad[bad.length - 1].t + 9 * 3600000).toISOString().slice(5, 16).replace('T', ' ') : '-';
    const codes = [...new Set(bad.map((r) => r.status))].slice(0, 3).join(',');
    console.log(`${m.padEnd(36)}${(100 * ok.length / rs.length).toFixed(1).padStart(6)}%${String(rs.length).padStart(7)}${String(bad.length).padStart(7)}${(lat + 'ms').padStart(10)}   ${last}${codes ? ` (${codes})` : ''}`);
  }
}

if (process.argv.includes('--report')) { report(); process.exit(0); }

const KEY = process.env.NOUS_API_KEY;
if (!KEY) { console.error('NOUS_API_KEY 없음'); process.exit(1); }

for (const model of MODELS) {
  const t0 = Date.now();
  let ok = false, status = 0, note = '';
  try {
    const r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      // 최소 요청 — 가용성만 본다. 비용은 턴당 $0.00001 미만.
      body: JSON.stringify({ model, messages: [{ role: 'user', content: 'ping' }], max_tokens: 4, reasoning: { enabled: false } }),
    });
    status = r.status;
    if (r.ok) { await r.json(); ok = true; } else { note = (await r.text()).slice(0, 100); }
  } catch (e) { note = String(e.message).slice(0, 100); }
  const rec = { t: Date.now(), model, ok, status, ms: Date.now() - t0, note: ok ? '' : note };
  appendFileSync(LOG, JSON.stringify(rec) + '\n');
  console.log(`${ok ? '✓' : '✗'} ${model.padEnd(36)} ${status || '-'} ${rec.ms}ms ${note.slice(0, 60)}`);
}
