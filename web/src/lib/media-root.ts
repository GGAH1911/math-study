// 기출 이미지의 **디스크 루트** — `public/` 밖이다.
//
// ★왜 public/ 밖인가: `public/` 안에 **있는** 파일은 정적 핸들러가 미들웨어보다 **먼저**
//   응답한다. 그래서 `middleware.ts` 의 인증 게이팅도, WebP 서빙도 실제 이미지 요청에는
//   닿지 못했다 — 기출 5,774장이 **무인증 200** 으로 열려 있었다(2026-08-14 실측:
//   `/problems` 는 302 인데 `/problem-images/2019_수능_가형_01.png` 는 200).
//   파일을 정적 서빙 밖으로 빼는 것만이 그 순서를 뒤집는 방법이다.
//
// ★공개 URL 은 `/problem-images/...` 그대로다. 본문·컴포넌트의 경로 문자열을 하나도
//   고치지 않으려고 **위치만** 옮겼다. 요청은 미들웨어가 받아 인증 뒤 여기서 읽어 준다.
//
// ★Phase 3(토큰 전환)과 분리했다. 로드맵은 이 수정을 "토큰 전환과 같은 릴리스" 로 묶었지만
//   그 전제는 **앱 클라이언트**(쿠키를 안 보냄)였다. 지금 클라이언트는 웹뿐이고 세션 쿠키가
//   살아 있으므로 미들웨어 게이팅만으로 닫힌다. Phase 3 이 오면 이 경로도 다른 라우트와
//   똑같이 베어러를 받으면 된다 — 어차피 Phase 3 이 전 라우트에 하는 일이다.
import { join, normalize, resolve } from 'node:path';

/** `web/private` — 정적 서빙이 닿지 않는 곳. `process.cwd()` 는 web/ (컨테이너: /app/web). */
export const MEDIA_ROOT = resolve(process.cwd(), 'private');

/**
 * 공개 URL 경로(`/problem-images/x.png`) → 디스크 절대경로.
 *
 * ⚠️ 경로 탈출 차단은 **인증과 별개 문제**다. `%2e%2e` 류로 리포 밖을 읽히면 안 된다.
 * 루트 밖으로 나가면 `null`.
 */
export function mediaPath(urlPath: string): string | null {
  let rel: string;
  try {
    rel = normalize(decodeURIComponent(urlPath)).replace(/^([/\\.]+)/, '');
  } catch {
    return null;                       // 잘못된 퍼센트 인코딩
  }
  const abs = join(MEDIA_ROOT, rel);
  return abs.startsWith(MEDIA_ROOT + '/') ? abs : null;
}
