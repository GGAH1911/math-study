#!/usr/bin/env node
// 기능 인벤토리 게이트 — "페이지에서 기능이 조용히 사라지는 것"을 막는다.
//
// ★왜 만들었나 (2026-08-15 실사고): Phase 3 SPA 전환 12호에서 개념 상세의 `<TutorChat>`
//   두 줄이 삭제됐고, **사장님이 화면을 보고 발견할 때까지 아무도 몰랐다.** 회귀 안전망
//   (`route_snapshot.mjs`)이 돌고 있었는데도 못 잡았다. 이유가 둘이다:
//
//   ① **숫자를 봤다.** `scripts 12→11` 은 SPA 전환 중엔 정당한 변화처럼 보인다.
//      `ChatPanel 있음→없음` 이었다면 변명의 여지가 없다.
//   ② **기준선을 단계마다 다시 떴다.** 12호에서 빠진 상태가 13호의 기준선이 되고,
//      그 뒤로는 영원히 "변화 없음"으로 통과한다. 차분 안전망의 구조적 한계다 —
//      **한 번 새어 들어온 결함은 그 다음부터 정상이 된다.**
//
// 그래서 이 게이트는 기준선을 **커밋된 파일**로 둔다. 기능이 줄면 막고, 정말 뺄 거면
// 기준선을 고치는 커밋에 이유를 적어야 통과한다 — 파일 크기 래칫과 같은 원리다.
//
// 사용:
//   T=$(node web/scripts/snapshot_session.mjs --mint)
//   node web/scripts/verify_feature_inventory.mjs --cookie "$T"            # 검사
//   node web/scripts/verify_feature_inventory.mjs --cookie "$T" --update   # 기준선 갱신
//
// 한계 셋 — 과신하지 말 것:
//   ① 마커도 섬도 아닌 순수 서버 렌더 UI 는 안 보인다. 새 기능엔 `data-*` 마커를 붙여라.
//   ② "렌더는 됐는데 동작 안 함" 은 못 잡는다(딥 헬스가 맡는 계열).
//   ③ ROUTES 22개 밖은 사각지대다.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { ROUTES, featuresOf } from './route_snapshot.mjs';

const args = process.argv.slice(2);
const arg = (k, d = null) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const has = (k) => args.includes(k);

const BASE = arg('--base', 'http://127.0.0.1:8080');
const BASELINE = arg('--baseline', new URL('../src/data/feature-inventory.json', import.meta.url).pathname);
const cookie = arg('--cookie');

async function collect() {
  const headers = cookie
    ? { cookie: cookie.includes('=') ? cookie : `ms_session=${cookie}` }
    : undefined;
  const out = {};
  for (const r of ROUTES) {
    try {
      const resp = await fetch(BASE.replace(/\/$/, '') + r, { redirect: 'manual', headers });
      const html = resp.status === 200 ? await resp.text() : '';
      out[r] = { status: resp.status, ...(html ? featuresOf(html) : { islands: [], markers: [] }) };
    } catch (e) {
      out[r] = { status: 0, islands: [], markers: [], error: String(e).slice(0, 80) };
    }
  }
  return out;
}

const now = await collect();

// ★빈 수집이 조용히 통과하는 것을 막는다. 전부 302 면 "로그인 화면 22장" 이고, 그건
//   자기들끼리는 일관돼서 **비교하면 늘 통과한다**(route_snapshot 이 같은 함정을 밟았다).
const ok200 = Object.values(now).filter((v) => v.status === 200).length;
if (ok200 === 0) {
  console.error('🔴 200 이 하나도 없다 — 기준으로 쓸 수 없다. --base 와 쿠키를 확인하라.');
  process.exit(1);
}

if (has('--update')) {
  writeFileSync(BASELINE, JSON.stringify(now, null, 1) + '\n', 'utf8');
  console.log(`✅ 기준선 갱신: ${BASELINE}  (200 ${ok200}개)`);
  console.log('   ⚠️ 기능을 **뺀** 갱신이라면 커밋 메시지에 이유를 적어라. 안 적으면 래칫이 아니다.');
  process.exit(0);
}

if (!existsSync(BASELINE)) {
  console.error(`🔴 기준선이 없다: ${BASELINE}\n   먼저 --update 로 만들어라.`);
  process.exit(1);
}
const base = JSON.parse(readFileSync(BASELINE, 'utf8'));

let lost = 0, gained = 0, statusBad = 0;
for (const r of Object.keys(base)) {
  const b = base[r], n = now[r] ?? { status: 0, islands: [], markers: [] };

  if (b.status === 200 && n.status !== 200) {
    console.log(`🔴 ${r}  status ${b.status}→${n.status}`);
    statusBad++;
    continue;   // 200 이 아니면 기능 비교는 의미가 없다
  }

  const missIsl = (b.islands ?? []).filter((x) => !(n.islands ?? []).includes(x));
  const missMk = (b.markers ?? []).filter((x) => !(n.markers ?? []).includes(x));
  const newIsl = (n.islands ?? []).filter((x) => !(b.islands ?? []).includes(x));
  const newMk = (n.markers ?? []).filter((x) => !(b.markers ?? []).includes(x));

  if (missIsl.length || missMk.length) {
    console.log(`🔴 ${r}`);
    if (missIsl.length) console.log(`     사라진 섬:   ${missIsl.join(', ')}`);
    if (missMk.length) console.log(`     사라진 마커: ${missMk.join(', ')}`);
    lost += missIsl.length + missMk.length;
  }
  if (newIsl.length || newMk.length) {
    console.log(`🟢 ${r}  추가: ${[...newIsl, ...newMk].join(', ')}`);
    gained += newIsl.length + newMk.length;
  }
}

const unseen = Object.keys(now).filter((r) => !(r in base));
if (unseen.length) console.log(`🟡 기준선에 없는 라우트 ${unseen.length}개: ${unseen.join(', ')}`);

console.log(
  `\n라우트 ${Object.keys(base).length} · 200 ${ok200} · 사라짐 ${lost} · 추가 ${gained} · status회귀 ${statusBad}`,
);

if (lost || statusBad) {
  console.error(
    '\n🔴 기능이 사라졌다. 의도한 제거면 `--update` 로 기준선을 내리고 **커밋에 이유를 적어라**.',
  );
  process.exit(1);
}
if (gained) console.log('🟢 추가만 있다 — 통과. 원하면 `--update` 로 기준선을 올려 둬라.');
else console.log('✅ 기능 인벤토리 일치');
