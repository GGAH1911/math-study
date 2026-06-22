// Let's copy the relevant parts of the de-overlapping code from Geometry.tsx

function estLabelWidth(text, fontPx) {
  let t = String(text);
  t = t.replace(/\\(cos|sin|tan|sec|csc|cot|log|ln|lim|exp|max|min|sqrt|sup|inf|deg|arg|det|dim|gcd|lcm)\b/g,
                (_, w) => 'x'.repeat(w.length));
  t = t.replace(/\\[a-zA-Z]+/g, 'x');
  t = t.replace(/[{}$^_\\\s]/g, '');
  const n = Math.max(1, t.length);
  return Math.max(fontPx, n * fontPx * 0.6) + 8;
}

function _closestOnSeg(px, py, s) {
  const dx = s[2] - s[0], dy = s[3] - s[1];
  const len2 = dx * dx + dy * dy || 1;
  let t = ((px - s[0]) * dx + (py - s[1]) * dy) / len2;
  t = Math.max(0, Math.min(1, t));
  return [s[0] + t * dx, s[1] + t * dy];
}

function deOverlapLabels(descs, fontPx, W, H, obstacles = []) {
  const h = fontPx * 1.5;
  const MAXSHIFT = fontPx * 2;
  const PAD = 2;
  const boxes = descs.map((d) => {
    const w = estLabelWidth(d.text, fontPx);
    const x0 = d.left + (d.tx / 100) * w;
    return { d, w, h, x: x0, y: d.top, ox: x0, oy: d.top, fixed: !!d.fixed };
  });
  for (let iter = 0; iter < 90; iter++) {
    let moved = false;
    // 1) Labels overlap
    for (let a = 0; a < boxes.length; a++) {
      for (let b = a + 1; b < boxes.length; b++) {
        const A = boxes[a], B = boxes[b];
        if (A.fixed && B.fixed) continue;
        const ox = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
        const oy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ox > 0 && oy > 0) {
          moved = true;
          const wa = A.fixed ? 0 : (B.fixed ? 1 : 0.5), wb = B.fixed ? 0 : (A.fixed ? 1 : 0.5);
          const oldAx = A.x, oldBx = B.x;
          if (ox <= oy) { const p = ox + 0.5, dir = A.x <= B.x ? -1 : 1; A.x += dir * p * wa; B.x -= dir * p * wb; }
          else { const p = oy + 0.5, dir = A.y <= B.y ? -1 : 1; A.y += dir * p * wa; B.y -= dir * p * wb; }
          console.log(`[Iter ${iter}] Labels overlap: ${A.d.text} & ${B.d.text} moved from A.x=${oldAx.toFixed(1)}, B.x=${oldBx.toFixed(1)} to A.x=${A.x.toFixed(1)}, B.x=${B.x.toFixed(1)}`);
        }
      }
    }
    // 2) Obstacles overlap
    for (const box of boxes) {
      if (box.fixed) continue;
      const cx = box.x + box.w / 2, cy = box.y + box.h / 2;
      for (const seg of obstacles) {
        const [qx, qy] = _closestOnSeg(cx, cy, seg);
        const inX = qx > box.x - PAD && qx < box.x + box.w + PAD;
        const inY = qy > box.y - PAD && qy < box.y + box.h + PAD;
        if (inX && inY) {
          moved = true;
          const dl = qx - (box.x - PAD), dr = (box.x + box.w + PAD) - qx;
          const dt = qy - (box.y - PAD), db = (box.y + box.h + PAD) - qy;
          const m = Math.min(dl, dr, dt, db);
          const oldX = box.x, oldY = box.y;
          if (m === dl) box.x += dl + 1; else if (m === dr) box.x -= dr + 1;
          else if (m === dt) box.y += dt + 1; else box.y -= db + 1;
          console.log(`[Iter ${iter}] Obstacle overlap: ${box.d.text} moved from (${oldX.toFixed(1)}, ${oldY.toFixed(1)}) to (${box.x.toFixed(1)}, ${box.y.toFixed(1)}) due to seg ${seg.map(n => n.toFixed(1)).join(',')}`);
        }
      }
    }
    if (!moved) break;
  }
  return boxes.map(({ d, w, h: bh, x, y, ox, oy }) => {
    let nx = Math.max(ox - MAXSHIFT, Math.min(ox + MAXSHIFT, x));
    let ny = Math.max(oy - MAXSHIFT, Math.min(oy + MAXSHIFT, y));
    nx = Math.max(0, Math.min(W - w, nx));
    ny = Math.max(0, Math.min(H - bh, ny));
    return { ...d, left: d.left + (nx - ox), top: d.top + (ny - oy), finalX: nx, finalY: ny };
  });
}

// Set up the coordinate translation for W=380, H=380, range=[-2.5, 2.5], yRange=[-4.5, 4.5]
const W = 380;
const H = 380;
const xMin = -2.5, xMax = 2.5;
const yMin = -4.5, yMax = 4.5;

function xPx(x) {
  return ((x - xMin) / (xMax - xMin)) * W;
}
function yPx(y) {
  return H - ((y - yMin) / (yMax - yMin)) * H;
}

const labelFontPx = 14;

// Obstacles:
const obstacles = [
  [xPx(-2.2), yPx(2), xPx(2.2), yPx(2)],
  [xPx(-2.2), yPx(-2), xPx(2.2), yPx(-2)],
  [xPx(-2.2), yPx(1), xPx(2.2), yPx(1)],
];

const shapes = [
  { type: 'text', at: [-1.7, 3.2], text: 'y=f(x)' },
  { type: 'text', at: [2.3, 2], text: 'y=M' },
  { type: 'text', at: [2.3, 1], text: 'y=c' },
  { type: 'text', at: [2.3, -2], text: 'y=m' },
  { type: 'point', at: [-1.53209, 1], label: 'P_1', labelDir: 'NW' },
  { type: 'point', at: [-0.3473, 1], label: 'P_2', labelDir: 'NE' },
  { type: 'point', at: [1.8794, 1], label: 'P_3', labelDir: 'NW' },
];

const labelDescs = [];

shapes.forEach((s, i) => {
  if (s.type === 'text') {
    labelDescs.push({
      key: `tx${i}`,
      text: s.text,
      left: xPx(s.at[0]) + 4,
      top: yPx(s.at[1]) - 8,
      tx: 0,
      anchor: [xPx(s.at[0]) + 4, yPx(s.at[1]) - 8]
    });
  } else if (s.type === 'point') {
    const [x, y] = s.at;
    const dir = s.labelDir ?? 'NE';
    const offX = dir.includes('E') ? 7 : (dir.includes('W') ? -7 : 0);
    const offY = dir.includes('N') ? -labelFontPx - 3 : (dir.includes('S') ? 7 : -labelFontPx / 2 - 2);
    const tx = dir.includes('W') ? -100 : (dir.includes('E') ? 0 : -50);
    labelDescs.push({
      key: `pl${i}`,
      text: s.label,
      left: xPx(x) + offX,
      top: yPx(y) + offY,
      tx,
      anchor: [xPx(x), yPx(y)]
    });
  }
});

console.log("INITIAL LABEL DESCS (W=380):");
labelDescs.forEach(d => {
  console.log(`${d.key} (${d.text}): left=${d.left.toFixed(1)}, top=${d.top.toFixed(1)}, tx=${d.tx}`);
});

const resolved = deOverlapLabels(labelDescs, labelFontPx, W, H, obstacles);

console.log("\nRESOLVED LABEL DESCS (W=380):");
resolved.forEach(d => {
  console.log(`${d.key} (${d.text}): left=${d.left.toFixed(1)}, top=${d.top.toFixed(1)}, finalX=${d.finalX.toFixed(1)}, finalY=${d.finalY.toFixed(1)}`);
});

