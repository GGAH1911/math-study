// 손그림 도형 인식 (스케치-후-스냅 UX의 핵심) — 순수 기하 함수, ML 불필요.
//   입력: 한 획의 점 배열(좌표). 출력: 인식된 도형(파라미터) 또는 null.
//   알고리즘: 닫힘 판정 + 곡률 기반 코너 검출 + ★코너 사이 엣지 직선성(다각형 vs 타원/원 결정).
//   검증: 합성 도형(직선·삼각형·사각형·원·타원) 5/5 분류(scratchpad/shape_test.mjs).
//   ★다음 단계(사장님과): 인식 결과 → 깔끔한 파라메트릭 도형으로 스냅 + 1탭 확정 + InteractiveSpec 슬라이더.
//   스펙: docs/architecture/handwriting-canvas.md (Phase C).

export type P = { x: number; y: number };
export type RecShape =
  | { kind: 'line'; a: P; b: P }
  | { kind: 'polyline'; pts: P[] }
  | { kind: 'circle'; cx: number; cy: number; r: number }
  | { kind: 'ellipse'; cx: number; cy: number; rx: number; ry: number }
  | { kind: 'triangle'; pts: P[] }
  | { kind: 'rect'; x: number; y: number; w: number; h: number }
  | { kind: 'polygon'; pts: P[] };

const dist = (a: P, b: P) => Math.hypot(a.x - b.x, a.y - b.y);
const perpDist = (p: P, a: P, b: P) => {
  const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
  return len === 0 ? dist(p, a) : Math.abs((p.x - a.x) * dy - (p.y - a.y) * dx) / len;
};
const bbox = (pts: P[]) => {
  let a = Infinity, b = Infinity, c = -Infinity, d = -Infinity;
  for (const p of pts) { if (p.x < a) a = p.x; if (p.y < b) b = p.y; if (p.x > c) c = p.x; if (p.y > d) d = p.y; }
  return { minX: a, minY: b, maxX: c, maxY: d, w: c - a, h: d - b };
};
// 꼭짓점 v 에서의 내각(도). 직선=180, 직각=90.
const angleAt = (prev: P, v: P, next: P) => {
  const a1 = Math.atan2(prev.y - v.y, prev.x - v.x), a2 = Math.atan2(next.y - v.y, next.x - v.x);
  let dd = Math.abs(a1 - a2); if (dd > Math.PI) dd = 2 * Math.PI - dd;
  return (dd * 180) / Math.PI;
};

// 곡률 기반 코너: 창 k 내각이 임계 미만이면 sharp, 인접 sharp 를 클러스터링해 코너 1개로.
function cornerInfo(pts: P[], closed: boolean): { count: number; verts: P[]; idxs: number[] } {
  const n = pts.length, k = Math.max(2, Math.round(n * 0.06));
  const ang = new Array<number>(n).fill(180);
  for (let i = 0; i < n; i++) { if (!closed && (i < k || i >= n - k)) continue; ang[i] = angleAt(pts[(i - k + n) % n], pts[i], pts[(i + k) % n]); }
  const sharp = ang.map((a) => a < 148);
  const s = sharp.findIndex((x) => !x); if (s < 0) return { count: 1, verts: [], idxs: [] }; // 전부 sharp = 뭉친 점
  const clusters: number[][] = []; let cur: number[] | null = null;
  for (let j = 0; j < n; j++) { const idx = (s + j) % n; if (sharp[idx]) { if (!cur) cur = []; cur.push(idx); } else if (cur) { clusters.push(cur); cur = null; } }
  if (cur) clusters.push(cur);
  const idxs = clusters.map((cl) => { let best = cl[0]; for (const idx of cl) if (ang[idx] < ang[best]) best = idx; return best; });
  return { count: clusters.length, verts: idxs.map((i) => pts[i]), idxs };
}
// 코너 사이 호가 직선(다각형) vs 곡선(타원/원) — 결정적 판별자.
function edgesStraight(pts: P[], idxs: number[], closed: boolean): boolean {
  const n = pts.length, m = idxs.length;
  for (let c = 0; c < (closed ? m : m - 1); c++) {
    const i0 = idxs[c], i1 = idxs[(c + 1) % m], a = pts[i0], b = pts[i1], chord = dist(a, b);
    if (chord < 6) continue;
    let maxD = 0, cnt = 0;
    for (let j = (i0 + 1) % n; j !== i1 && cnt <= n; j = (j + 1) % n) { maxD = Math.max(maxD, perpDist(pts[j], a, b)); cnt++; }
    if (maxD / chord > 0.14) return false; // 엣지가 휘어 있음
  }
  return true;
}

/** 한 획(점 배열)을 도형으로 인식. 인식 불가(자유 필기)면 null. */
export function recognizeShape(raw: P[]): RecShape | null {
  if (raw.length < 2) return null;
  if (raw.length < 6) return { kind: 'line', a: raw[0], b: raw[raw.length - 1] };
  const bb = bbox(raw), diag = Math.hypot(bb.w, bb.h); if (diag < 8) return null;
  const closed = dist(raw[0], raw[raw.length - 1]) < diag * 0.2;

  if (!closed) {
    const a = raw[0], b = raw[raw.length - 1];
    let maxD = 0; for (const p of raw) maxD = Math.max(maxD, perpDist(p, a, b));
    if (maxD < diag * 0.08) return { kind: 'line', a, b }; // 거의 직선
    const { count, verts } = cornerInfo(raw, false);
    if (count >= 1 && count <= 6) return { kind: 'polyline', pts: [a, ...verts, b] }; // 꺾은선
    return null;
  }

  const { count: nC, verts, idxs } = cornerInfo(raw, true);
  let cx = 0, cy = 0; for (const p of raw) { cx += p.x; cy += p.y; } cx /= raw.length; cy /= raw.length;
  const straight = nC >= 3 && nC <= 8 && edgesStraight(raw, idxs, true);
  if (nC <= 2 || !straight) { // 매끈한 닫힌 곡선 → 원/타원
    const asp = bb.w / bb.h;
    return asp > 0.78 && asp < 1.28
      ? { kind: 'circle', cx, cy, r: (bb.w + bb.h) / 4 }
      : { kind: 'ellipse', cx, cy, rx: bb.w / 2, ry: bb.h / 2 };
  }
  if (nC === 3) return { kind: 'triangle', pts: verts };
  if (nC === 4) {
    let rect = true;
    for (let i = 0; i < 4; i++) if (Math.abs(angleAt(verts[(i + 3) % 4], verts[i], verts[(i + 1) % 4]) - 90) > 22) rect = false;
    return rect ? { kind: 'rect', x: bb.minX, y: bb.minY, w: bb.w, h: bb.h } : { kind: 'polygon', pts: verts };
  }
  return { kind: 'polygon', pts: verts };
}

/** 인식된 도형 → 깔끔한 점 배열(스트로크로 그리기 위함). 원/타원은 둘레 샘플. */
export function shapeToPoints(s: RecShape): P[] {
  const arc = (cx: number, cy: number, rx: number, ry: number) => {
    const r: P[] = []; for (let i = 0; i <= 48; i++) { const t = (i / 48) * 2 * Math.PI; r.push({ x: cx + rx * Math.cos(t), y: cy + ry * Math.sin(t) }); } return r;
  };
  switch (s.kind) {
    case 'line': return [s.a, s.b];
    case 'polyline': return s.pts;
    case 'triangle': return [...s.pts, s.pts[0]];
    case 'polygon': return [...s.pts, s.pts[0]];
    case 'rect': return [{ x: s.x, y: s.y }, { x: s.x + s.w, y: s.y }, { x: s.x + s.w, y: s.y + s.h }, { x: s.x, y: s.y + s.h }, { x: s.x, y: s.y }];
    case 'circle': return arc(s.cx, s.cy, s.r, s.r);
    case 'ellipse': return arc(s.cx, s.cy, s.rx, s.ry);
  }
}
