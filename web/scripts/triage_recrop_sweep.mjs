#!/usr/bin/env node
// 레거시 크롭 일괄 정리: figure 보유 모든 문제를 현재 extract_figures 로직으로 재추출+frontmatter 동기화.
// 안전: extract_figures만 (솔루션 미접촉). 결정적. git 되돌림 가능.
// 로그: /tmp/ingest_logs/recrop_<stamp>.log (덮어쓰기 금지=타임스탬프 파일명)
import { readFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = join(__dirname, '..', '..');
const idx = JSON.parse(readFileSync(join(REPO, 'web/src/data/figure-triage.json'), 'utf-8'));
const SUBJ = ['확률과통계', '미적분', '가형', '나형', '기하', '단일', '공통']; // 긴 토큰 우선
const slugs = [...new Set(Object.values(idx.figures).map((f) => f.problem_slug))].sort();

const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const LOGDIR = '/tmp/ingest_logs';
if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const LOG = `${LOGDIR}/recrop_${stamp}.log`;
const log = (m) => { const line = `[${new Date().toISOString().slice(11, 19)}] ${m}`; console.log(line); appendFileSync(LOG, line + '\n'); };

const LIMIT = process.argv[2] ? Number(process.argv[2]) : slugs.length; // 옵션: 앞 N개만(테스트)
const targets = slugs.slice(0, LIMIT);
log(`recrop sweep 시작: ${targets.length}/${slugs.length} problems · log=${LOG}`);

let ok = 0, fail = 0, i = 0;
for (const slug of targets) {
  i++;
  let subj = null;
  for (const s of SUBJ) { if (slug.includes('_' + s + '_')) { subj = s; break; } }
  if (!subj) { log(`SKIP(subj?) ${slug}`); fail++; continue; }
  const parts = slug.split('_' + subj + '_');
  const round = parts[0], num = parts.slice(1).join('_' + subj + '_');
  try {
    execFileSync('python3', [join(REPO, 'web/scripts/extract_figures.py'), round, subj, num, '--apply'],
      { cwd: REPO, stdio: 'pipe', timeout: 90000 });
    ok++;
  } catch (e) {
    fail++;
    log(`FAIL ${slug}: ${(e.stderr || e.message || '').toString().replace(/\n/g, ' ').slice(0, 140)}`);
  }
  if (i % 50 === 0) log(`진행 ${i}/${targets.length} (ok ${ok} · fail ${fail})`);
}
log(`완료: ok ${ok} · fail ${fail} / ${targets.length}. 다음: triage_index.mjs 재빌드`);
