#!/usr/bin/env node
/**
 * Sync docs/assets/ -> public/assets/ so SVGs referenced from markdown
 * (D16 generator outputs) are served by Astro.
 */
import { cpSync, mkdirSync, existsSync, rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const SRC = join(WEB_ROOT, '..', 'docs', 'assets');
const DST = join(WEB_ROOT, 'public', 'assets');

if (existsSync(DST)) rmSync(DST, { recursive: true, force: true });
if (!existsSync(SRC)) {
  console.log(`[sync-assets] no docs/assets directory, skipping`);
  process.exit(0);
}
mkdirSync(DST, { recursive: true });
cpSync(SRC, DST, { recursive: true });
console.log(`[sync-assets] copied docs/assets/ -> public/assets/`);
