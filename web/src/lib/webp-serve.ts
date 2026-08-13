// 기출 이미지 WebP 서빙 — **파일을 개명하지도, 새로 커밋하지도 않는다.**
//
// ★왜 이 방식인가: 본문·코드에 박힌 경로 문자열은 4,164파일 13,819곳이다. 지금 개명하면
//   그 일괄 치환이 Phase 5(매니페스트·내용주소)와 두 번 겹친다. 그래서 **요청 경로는 .png 그대로**
//   두고, 서빙할 때만 WebP 로 바꿔 준다. Phase 5 에서 파일이 실제로 바뀌어도 이 계층만 걷어내면 된다.
//
// ★왜 무손실인가: 표본 30장 실측에서 무손실 39.6%, 손실 q90 34.9% 였다. 4.7%p 더 줄자고
//   수식 획·점선을 손실 압축에 맡길 이유가 없다.
//   재현: `python3 web/scripts/measure/webp_ratio.py`
//
// 변환은 **첫 요청 때 한 번**, 결과는 디스크에 캐시(.cache/webp, gitignore). 리포에 5,728개
// 파일을 더하지 않으려는 선택이다 — Phase 5 까지 PNG 와 WebP 를 둘 다 버전관리하면 리포가 두 배가 된다.
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, readFile, rename, stat, writeFile } from 'node:fs/promises';
import { dirname, join, normalize, resolve } from 'node:path';

const PUBLIC_DIR = resolve(process.cwd(), 'public');
const CACHE_DIR = resolve(process.cwd(), '.cache/webp');
const CONVERTIBLE = /\.(png|jpe?g)$/i;

/** 같은 파일을 동시에 변환하지 않도록 — 첫 요청 폭주 시 sharp 프로세스가 겹치는 걸 막는다. */
const inflight = new Map<string, Promise<Buffer | null>>();

async function convert(srcAbs: string, cacheAbs: string): Promise<Buffer | null> {
  const existing = inflight.get(cacheAbs);
  if (existing) return existing;
  const job = (async () => {
    try {
      const { default: sharp } = await import('sharp');
      const buf = await sharp(srcAbs).webp({ lossless: true, effort: 5 }).toBuffer();
      await mkdir(dirname(cacheAbs), { recursive: true });
      // ★.part 로 쓰고 rename — 중간에 죽어도 반쪽 파일이 캐시로 남지 않는다.
      const part = `${cacheAbs}.part.${process.pid}`;
      await writeFile(part, buf);
      await rename(part, cacheAbs);
      return buf;
    } catch {
      return null;   // 변환 실패는 조용히 포기 → 호출측이 원본 PNG 로 폴백
    }
  })();
  inflight.set(cacheAbs, job);
  try { return await job; } finally { inflight.delete(cacheAbs); }
}

/**
 * WebP 로 줄 수 있으면 Response, 아니면 null(호출측이 원본을 그대로 서빙).
 *
 * ⚠️ 경로는 반드시 정규화 후 PUBLIC_DIR 안인지 확인한다 — `%2e%2e` 류로 리포 밖 파일을
 *    읽히면 안 된다. 이 함수는 인증 통과 뒤에 불리지만, 경로 검사는 인증과 별개 문제다.
 */
export async function tryServeWebp(pathname: string, request: Request): Promise<Response | null> {
  if (!CONVERTIBLE.test(pathname)) return null;
  if (!(request.headers.get('accept') ?? '').includes('image/webp')) return null;

  const rel = normalize(decodeURIComponent(pathname)).replace(/^([/\\.]+)/, '');
  const srcAbs = join(PUBLIC_DIR, rel);
  if (!srcAbs.startsWith(PUBLIC_DIR + '/') || !existsSync(srcAbs)) return null;

  const cacheAbs = join(CACHE_DIR, `${rel}.webp`);
  let buf: Buffer | null = null;
  try {
    // 원본이 캐시보다 새로우면 다시 만든다(재크롭·재인제스트로 이미지가 바뀌는 일이 실제로 있다).
    const [s, c] = await Promise.all([stat(srcAbs), stat(cacheAbs).catch(() => null)]);
    if (c && c.mtimeMs >= s.mtimeMs) buf = await readFile(cacheAbs);
  } catch { /* 캐시 미스 → 아래에서 변환 */ }
  if (!buf) buf = await convert(srcAbs, cacheAbs);
  if (!buf) return null;

  const etag = `W/"${createHash('sha1').update(buf).digest('hex').slice(0, 16)}"`;
  if (request.headers.get('if-none-match') === etag) {
    return new Response(null, { status: 304, headers: { etag, vary: 'Accept' } });
  }
  return new Response(new Uint8Array(buf), {
    headers: {
      'content-type': 'image/webp',
      'content-length': String(buf.byteLength),
      // ★Vary: Accept 가 없으면 중간 캐시가 WebP 응답을 미지원 클라이언트에 물려 준다.
      vary: 'Accept',
      etag,
      'cache-control': 'private, max-age=3600, must-revalidate',
    },
  });
}
