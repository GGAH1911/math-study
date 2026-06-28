// 캐시 친화 `claude -p` 러너 — 앞으로 claude -p 를 쓰는 모든 스크립트는 이걸 거쳐라.
// 핵심: 레포 cwd 에서 돌리면 git status(미커밋 변경)가 매 호출 시스템 프롬프트의 env 블록을
// 바꿔 프롬프트 캐시를 깬다(실측 콜당 ~17k 토큰 재기록). 깨끗한 빈 cwd 에서 실행 → prefix 안정 →
// cache_read 살아남(~76% 입력비용 절감). 파일 접근은 addDirs(--add-dir, 절대경로)로.
//
// 사용:
//   import { claudeP } from './lib/claude_p.mjs';
//   const { result, usage } = await claudeP({ prompt, model: 'sonnet', system: FIXED_SYS, addDirs: [imgDir] });
//   // usage.cache_read_input_tokens 로 캐시 히트 확인. 호출은 5분 TTL 안에 연달아 쏠수록 캐시 유지.
//
// 캐싱 더 살리려면: ① 고정 지시문은 system(--system-prompt)으로 빼라(base 와 함께 캐시) ②가변부
//   (개념내용·이미지)는 prompt(user)로 ③ 호출을 연사(TTL 5분) ④ 더 확실하면 API 직접(cache_control).
import { spawn } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';

const CLEAN_DIR = process.env.CLAUDE_P_CWD || '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

export function claudeP({ prompt, model = 'sonnet', system = null, addDirs = [], maxTurns = 1, timeoutMs = 180000 }) {
  return new Promise((resolve, reject) => {
    const args = ['-p', prompt, '--model', model, '--output-format', 'json', '--max-turns', String(maxTurns)];
    if (system) args.push('--system-prompt', system);
    for (const d of addDirs) args.push('--add-dir', d);
    // ★clean cwd(벨트)만으론 git 블록이 새어 cache_creation 만 잡히는 경우 있음 → DISABLE_GIT(멜빵) 동시.
    const c = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    let out = '', err = '';
    const to = setTimeout(() => { try { c.kill('SIGKILL'); } catch {} reject(new Error('claude -p timeout')); }, timeoutMs);
    c.stdout.on('data', (d) => (out += d));
    c.stderr.on('data', (d) => (err += d));
    c.on('close', () => {
      clearTimeout(to);
      try { const j = JSON.parse(out); resolve({ result: j.result ?? '', usage: j.usage ?? {}, raw: j }); }
      catch { reject(new Error('claude -p parse fail: ' + (err || out).slice(0, 300))); }
    });
    c.on('error', (e) => { clearTimeout(to); reject(e); });
  });
}

export { CLEAN_DIR };
