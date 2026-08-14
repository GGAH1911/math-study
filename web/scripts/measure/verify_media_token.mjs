// 미디어 토큰 위조 방어 테스트 — 8케이스 적대적 검증.
//   실행: cd web && node --experimental-strip-types scripts/measure/verify_media_token.mjs
//   (비밀은 이 파일에서 테스트용으로만 주입한다. 운영 비밀 MS_MEDIA_JWT_SECRET 과 무관.)
//
// 막는 것: 서명 변조 · alg:none 바꿔치기 · alg 위장(HS512) · 페이로드 변조 ·
//          scope 변조 · 만료 · 빈 토큰. JWT 구현의 고전적 우회들이다.
process.env.MS_MEDIA_JWT_SECRET = "verification-only-secret-at-least-32-characters-long";
const m = await import("/home/insung/math-study/web/src/lib/media-token.ts");
const { issueMediaToken, verifyMediaToken } = m;
const { token } = issueMediaToken("user-123");
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64").replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
const [h, b, s] = token.split(".");
const cases = [
  ["정상 토큰",                token,                                   true ],
  ["서명 1바이트 변조",         h+"."+b+"."+(s.slice(0,-1)+(s.at(-1)==="A"?"B":"A")), false],
  ["alg:none 바꿔치기",        b64({alg:"none",typ:"JWT"})+"."+b+".",   false],
  ["alg:HS512 로 위장",        b64({alg:"HS512",typ:"JWT"})+"."+b+"."+s, false],
  ["페이로드 변조(sub 교체)",   h+"."+b64({sub:"attacker",scope:"media",jti:"x",iat:0,exp:9e9})+"."+s, false],
  ["scope 변조",              h+"."+b64({sub:"user-123",scope:"admin",jti:"x",iat:0,exp:9e9})+"."+s, false],
  ["만료됨",                  (()=>{const t=issueMediaToken("u",-10);return t.token})(), false],
  ["빈 토큰",                 "",                                      false],
];
let pass=0;
for (const [name, tok, want] of cases) {
  const got = verifyMediaToken(tok) !== null;
  const ok = got === want;
  if (ok) pass++;
  console.log(`  ${ok?"✅":"❌"} ${name.padEnd(22)} 검증통과=${got} (기대 ${want})`);
}
console.log(`\n${pass}/${cases.length} 통과`);
process.exit(pass === cases.length ? 0 : 1);
