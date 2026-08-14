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
import { mkdirSync, existsSync, readFileSync } from 'node:fs';

const CLEAN_DIR = process.env.CLAUDE_P_CWD || '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

// ★구독 인증 — `scripts/claude_auth.py` 의 node 판. 어긋나면 한쪽만 조용히 죽는다.
//   인증이 없으면 claude 는 "Not logged in" **한 줄만 뱉고 exit 0** 이다. 반환코드가 0이라
//   호출부는 그냥 '파싱실패'로 보고, 재시도까지 실패한 뒤 데이터를 격리한다 — 인증 문제인 줄
//   아무도 모른다(2026-08-14 실측: 교정기가 이 경로로 문항을 격리했다).
const REPO_ROOT = process.env.MATHSTUDY_ROOT || new URL('../../..', import.meta.url).pathname.replace(/\/$/, '');
function oauthToken() {
  if (process.env.CLAUDE_CODE_OAUTH_TOKEN) return process.env.CLAUDE_CODE_OAUTH_TOKEN;
  try {
    const m = readFileSync(`${REPO_ROOT}/deploy/.env`, 'utf8').match(/^MS_CLAUDE_OAUTH_TOKEN=(.*)$/m);
    return m ? m[1].trim() : '';
  } catch { return ''; }
}
const OAUTH = oauthToken();

/** claude -p 서브프로세스용 env — 캐시 안정(git 블록 제거) + 구독 토큰 주입. */
export function claudeEnv(base = process.env) {
  return { ...base, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1', ...(OAUTH ? { CLAUDE_CODE_OAUTH_TOKEN: OAUTH } : {}) };
}

/** 인증 실패 감지 — exit 0 이라 본문을 봐야 한다. */
export function looksUnauthed(s) {
  return /Not logged in|Invalid API key/i.test(s || '');
}

export function claudeP({ prompt, model = 'sonnet', system = null, addDirs = [], maxTurns = 1, timeoutMs = 180000 }) {
  return new Promise((resolve, reject) => {
    const args = ['-p', prompt, '--model', model, '--output-format', 'json', '--max-turns', String(maxTurns)];
    if (system) args.push('--system-prompt', system);
    for (const d of addDirs) args.push('--add-dir', d);
    // ★clean cwd(벨트)만으론 git 블록이 새어 cache_creation 만 잡히는 경우 있음 → DISABLE_GIT(멜빵) 동시.
    const c = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: claudeEnv() });
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
