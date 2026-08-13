// Node ESM 해석 훅 — 확장자 없는 상대 import 를 .ts/.tsx/.js 로 풀어 준다.
//   앱 코드는 Vite(Astro) 해석 규칙에 맞춰 `./foo` 처럼 쓰는데, 순수 node 는 확장자를 요구해
//   ERR_MODULE_NOT_FOUND 가 난다. 평가·측정 스크립트가 **프로덕션과 같은 모듈**(buildTutorPrompt 등)을
//   그대로 import 하려면 이 훅이 필요하다(프롬프트를 복붙하면 그 순간 측정이 프로덕션과 갈라진다).
// 사용: node --experimental-strip-types --import ./web/scripts/ts-resolve-hook.mjs <script>
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';

if (!process.env.__TS_HOOK_REGISTERED) {
  process.env.__TS_HOOK_REGISTERED = '1';
  register(pathToFileURL(import.meta.filename ?? import.meta.url));
}

const EXTS = ['.ts', '.tsx', '.mts', '.js', '.mjs', '/index.ts', '/index.js'];

// JSON 은 Vite 가 그냥 import 시켜 주지만 node 는 `with { type: 'json' }` 을 요구한다.
// 앱 코드를 고칠 순 없으니(프로덕션 경로) 훅에서 속성을 붙여 준다.
const withJson = (r) => (r?.url?.endsWith('.json') ? { ...r, importAttributes: { type: 'json' } } : r);

export async function resolve(specifier, context, next) {
  try {
    return withJson(await next(specifier, context));
  } catch (err) {
    if (!specifier.startsWith('.') && !specifier.startsWith('/')) throw err;
    if (/\.[a-z]+$/i.test(specifier)) throw err;   // 이미 확장자가 있으면 진짜 없는 것
    for (const ext of EXTS) {
      try { return withJson(await next(specifier + ext, context)); } catch { /* 다음 후보 */ }
    }
    throw err;
  }
}
