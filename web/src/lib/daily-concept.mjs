// 「오늘의 개념」 — 매일 새로운 개념 하나를 전체 개념 풀에서 고른다(곡선 6종 돌리기 아님).
// 고정 시드로 한 번 섞은 순열을 KST 연속 일수로 하루에 하나씩 순회 → 풀 전체를 한 바퀴 돌기
// 전엔 안 겹치고(개념 수천 개 → 수년치), 인접일은 서로 다른 주제가 나오도록 셔플돼 있다.

// KST 연속 일수(자정마다 +1).
export function kstEpochDay(nowMs) {
  return Math.floor((nowMs + 9 * 3600 * 1000) / 86400000);
}

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// 결정적 Fisher–Yates 순열(고정 시드) — 매 호출 같은 순서.
function shuffledIndices(n, seed) {
  const rnd = mulberry32(seed);
  const a = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    const tmp = a[i]; a[i] = a[j]; a[j] = tmp;
  }
  return a;
}

// nodes = readConceptGraph().nodes. 오늘의 개념 노드 1개 반환(없으면 null).
export function pickDailyConcept(nodes, nowMs) {
  // 진짜 '개념'만: 정의(definition)·정리(theorem). 예제(example)·단원(unit) 컨테이너는 제외.
  // (정의 2698 + 정리 102 ≈ 2800개 → 한 바퀴 도는 데 수년, 매일 새 개념.)
  const pool = (nodes ?? []).filter(
    (n) => n && n.label && n.id && (n.concept_type === 'definition' || n.concept_type === 'theorem'),
  );
  if (!pool.length) return null;
  // id 안정 정렬 → 콘텐츠가 늘어도 같은 날 같은 개념(결정적). 고정 시드로 섞어 인접일 다양성 확보.
  const sorted = pool.slice().sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  const perm = shuffledIndices(sorted.length, 0x5eed1234);
  const day = ((kstEpochDay(nowMs) % sorted.length) + sorted.length) % sorted.length;
  return sorted[perm[day]];
}
