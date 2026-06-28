#!/usr/bin/env node
// =============================================================================
// 📝 Index Generator — per-directory 00_<DIR>.md 자동생성/갱신 (docs + 소스코드)
// =============================================================================
// TME 토폴로지를 docs 뿐 아니라 소스(web/src·scripts)까지 확장 → 설계(docs)부터 구현(code)까지
// 같은 인덱스 망으로 연결(spec→module traverse). 규칙:
//   - docs/: .md 나열, 콘텐츠 메시(concepts 등)는 제외(audit-lwip 관할).
//   - web/src·scripts: 소스 파일(.ts/.tsx/.astro/.mjs/.css/.py) 나열. 인덱스 자체는 .md(LWIP 규약).
//     ★content collection 은 docs/ 만 glob 하므로 src 의 00_*.md 는 Astro 가 안 건드림(검증됨).
//   - <!-- AUTO_INDEX_SECTION --> ~ 다음 '---' 사이만 재생성. 그 위 제목·아래 수동 설명/링크는 보존.
//   - 사람이 쓴 설명(`- \`file\` — 설명`)은 파일이 남아있으면 유지.
//   - ★이름 충돌: 같은 폴더명(예: lib/chat·components/chat)은 00_<DIR> 가 겹침 → 2-패스로 감지해
//     겹치는 폴더만 부모 접두(00_LIB_CHAT·00_COMPONENTS_CHAT). 안 겹치면 00_<DIR> 유지(짧게).
// prebuild/predev 체인에서 audit-lwip 와 함께 실행.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '../..');

const EXCLUDE_DIR = new Set(['node_modules', '.git', '.obsidian', '__pycache__', '.astro', 'dist', 'build', '.vercel']);
const MARK = '<!-- AUTO_INDEX_SECTION -->';

// 인덱싱 루트들. exts=나열할 파일 확장자, excludeTop=루트 직속 제외 폴더, rootParent=루트 인덱스의 상위 링크.
const ROOTS = [
  {
    dir: path.join(REPO, 'docs'), exts: ['.md'], rootParent: '[[index]]',
    excludeTop: new Set(['concepts', 'problems', 'hubs', 'mistakes', 'notes', 'syntheses', 'paths', '_archive', 'assets']),
  },
  {
    dir: path.join(REPO, 'web', 'src'), exts: ['.ts', '.tsx', '.astro', '.mjs', '.css'],
    rootParent: '[[00_ARCHITECTURE|docs/architecture/]]', excludeTop: new Set(),
  },
  {
    dir: path.join(REPO, 'scripts'), exts: ['.py', '.mjs'],
    rootParent: '[[00_ARCHITECTURE|docs/architecture/]]', excludeTop: new Set(),
  },
];

const upper = (s) => s.toUpperCase().replace(/[^A-Z0-9]+/g, '_');

// ── PASS 1 ─────────────────────────────────────────────────────────────────
// 인덱스를 가질 폴더(파일 또는 live 하위폴더 보유)를 전부 수집.
const liveDirs = [];
function collectLive(dir, cfg, isTop) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const subDirs = entries
    .filter((e) => e.isDirectory() && !EXCLUDE_DIR.has(e.name))
    .filter((e) => !(isTop && cfg.excludeTop.has(e.name)))
    .map((e) => e.name);
  const hasFiles = entries.some((e) => e.isFile() && !e.name.startsWith('00_') && cfg.exts.some((x) => e.name.endsWith(x)));
  let anyLiveChild = false;
  for (const sd of subDirs) if (collectLive(path.join(dir, sd), cfg, false)) anyLiveChild = true;
  const live = hasFiles || anyLiveChild;
  if (live) liveDirs.push(dir);
  return live;
}
for (const cfg of ROOTS) if (fs.existsSync(cfg.dir)) collectLive(cfg.dir, cfg, true);

// base 이름(00_<DIR>) 별 그룹 → 2+ 면 부모 접두로 충돌 해소.
const STEM = new Map();   // dir(abs) → 00_STEM
{
  const byBase = new Map();
  for (const d of liveDirs) {
    const b = upper(path.basename(d));
    if (!byBase.has(b)) byBase.set(b, []);
    byBase.get(b).push(d);
  }
  for (const [b, ds] of byBase) {
    if (ds.length === 1) STEM.set(ds[0], `00_${b}`);
    else for (const d of ds) STEM.set(d, `00_${upper(path.basename(path.dirname(d)))}_${b}`);
  }
}
const stemOf = (dir) => STEM.get(dir) ?? `00_${upper(path.basename(dir))}`;
const nameOf = (dir) => `${stemOf(dir)}.md`;

// ── PASS 2 ─────────────────────────────────────────────────────────────────
let created = 0, updated = 0, removed = 0;

function existingDescriptions(text) {
  const map = new Map();
  for (const m of text.matchAll(/^- `([^`]+)`\s*(?:—\s*(.*))?$/gm)) map.set(m[1], (m[2] ?? '').trim());
  return map;
}

function buildSection(files, subDirs, dir, prevDesc) {
  const lines = [];
  for (const d of subDirs) lines.push(`- 📁 [[${stemOf(path.join(dir, d))}|${d}/]]`);
  for (const f of files) {
    const desc = prevDesc.get(f);
    lines.push(`- \`${f}\`${desc ? ` — ${desc}` : ' — 등록 자산'}`);
  }
  return lines.join('\n');
}

// 폴더의 스테일 자동인덱스(현재 resolved 이름이 아닌 00_*.md, 마커 보유=자동생성) 제거.
function removeStale(dir, keepName) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!e.isFile() || !e.name.startsWith('00_') || !e.name.endsWith('.md') || e.name === keepName) continue;
    const fp = path.join(dir, e.name);
    try { if (fs.readFileSync(fp, 'utf8').includes(MARK)) { fs.rmSync(fp); removed++; } } catch { /* noop */ }
  }
}

function processDir(dir, cfg, isTop, parentLink) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const subDirsAll = entries
    .filter((e) => e.isDirectory() && !EXCLUDE_DIR.has(e.name))
    .filter((e) => !(isTop && cfg.excludeTop.has(e.name)))
    .map((e) => e.name);
  const files = entries
    .filter((e) => e.isFile() && !e.name.startsWith('00_') && cfg.exts.some((x) => e.name.endsWith(x)))
    .map((e) => e.name)
    .sort();

  const myLink = `[[${stemOf(dir)}]]`;
  const liveSubDirs = [];
  for (const sd of subDirsAll) {
    if (processDir(path.join(dir, sd), cfg, false, myLink)) liveSubDirs.push(sd);
  }
  if (files.length === 0 && liveSubDirs.length === 0) return false;

  const name = nameOf(dir);
  removeStale(dir, name);                          // 옛 이름 인덱스 정리(충돌 해소로 rename된 경우)
  const idxPath = path.join(dir, name);
  const section = buildSection(files, liveSubDirs, dir,
    fs.existsSync(idxPath) ? existingDescriptions(fs.readFileSync(idxPath, 'utf8')) : new Map());

  if (!fs.existsSync(idxPath)) {
    const body = `---\nsources: []\ncreated: ${today()}\nupdated: ${today()}\n---\n\n# 📝 ${stemOf(dir)} (자동 생성 인덱스)\n> 분류: Wiki / Auto-Generated\n\n## 전수 명세\n\n${MARK}\n${section}\n\n---\n## 🔗 지식망 연결\n- **상위 분류**: ${parentLink}\n`;
    fs.writeFileSync(idxPath, body, 'utf8');
    created++;
    return true;
  }

  const cur = fs.readFileSync(idxPath, 'utf8');
  const mi = cur.indexOf(MARK);
  if (mi === -1) return true;
  const after = cur.indexOf('\n---', mi);
  const end = after === -1 ? cur.length : after;
  const next = cur.slice(0, mi + MARK.length) + '\n' + section + '\n' + cur.slice(end);
  if (next !== cur) { fs.writeFileSync(idxPath, next, 'utf8'); updated++; }
  return true;
}

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

for (const cfg of ROOTS) {
  if (fs.existsSync(cfg.dir)) processDir(cfg.dir, cfg, true, cfg.rootParent);
}
console.log(`[indices] created ${created} · updated ${updated} · removed(stale) ${removed}`);
