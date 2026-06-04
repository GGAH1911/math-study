// 클라이언트 전용 — 첨부 이미지 검증·HEIC 변환·리사이즈·크롭.
// window/FileReader/canvas/heic2any(브라우저 API)를 쓰므로 서버에서 import 금지.

export const ACCEPTED_MIME = ['image/png', 'image/jpeg', 'image/webp'];
export const MAX_INPUT_BYTES = 8 * 1024 * 1024;   // 입력 원본 상한
export const VISION_LONG_EDGE = 1568;             // Claude vision 긴 변 한도
export const VISION_AREA = 1_150_000;             // Claude vision 면적 한도(~1.15MP)
const TILE_TARGET = 1040;                         // 타일 셀 목표 변(≤1568, ~1.08MP)
const TILE_OVERLAP = 90;                          // 타일 경계 겹침(px)
const MAX_TILES = 6;                              // 자동 타일 상한 — 초과(초대형)는 크롭 폴백
                                                  // (2D는 ~16조각서 LLM 조립 실패 → 보수적으로)

export type Prepared =
  | { kind: 'ready'; dataUrls: string[] }         // 1장 또는 N타일(원해상도) → 바로 첨부
  | { kind: 'needsCrop'; rawDataUrl: string };    // 상한 초과(초대형) → 크롭 모달 폴백

const isHeic = (f: File) => /image\/hei[cf]/i.test(f.type) || /\.hei[cf]$/i.test(f.name);

async function heicToJpeg(file: File): Promise<Blob> {
  // HEIC 첨부 시에만 lazy load (~1.5MB WASM).
  const heic2any = (await import('heic2any')).default as
    (o: { blob: Blob; toType?: string; quality?: number }) => Promise<Blob | Blob[]>;
  const out = await heic2any({ blob: file, toType: 'image/jpeg', quality: 0.92 });
  return Array.isArray(out) ? out[0] : out;
}

function blobToDataUrl(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result as string);
    r.onerror = () => reject(new Error('이미지 읽기에 실패했습니다.'));
    r.readAsDataURL(blob);
  });
}

export function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('이미지를 디코드할 수 없습니다 (손상된 파일?).'));
    img.src = src;
  });
}

// (크롭 영역 또는 전체)를 긴 변 limit PNG dataURL 로. PNG 유지 = 재인코딩 손실 0.
function toPng(img: HTMLImageElement, sx: number, sy: number, sw: number, sh: number, limit: number): string {
  let w = sw, h = sh;
  const long = Math.max(w, h);
  if (long > limit) { const s = limit / long; w = Math.round(w * s); h = Math.round(h * s); }
  const canvas = document.createElement('canvas');
  canvas.width = Math.max(1, Math.round(w));
  canvas.height = Math.max(1, Math.round(h));
  canvas.getContext('2d')!.drawImage(img, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/png');
}

export const downscaleFull = (img: HTMLImageElement): string =>
  toPng(img, 0, 0, img.naturalWidth, img.naturalHeight, VISION_LONG_EDGE);

export const cropRegion = (img: HTMLImageElement, sx: number, sy: number, sw: number, sh: number): string =>
  toPng(img, sx, sy, sw, sh, VISION_LONG_EDGE);

const withinBudget = (w: number, h: number): boolean =>
  Math.max(w, h) <= VISION_LONG_EDGE && w * h <= VISION_AREA;

// 큰 이미지를 LLM(vision) 입력용 타일 dataURL 들로. 예산 내면 1장, 세로로만 길면
// 1D(세로 분할), 가로·세로 둘 다 크면 2D 격자 — 각 타일이 1568·1.15MP 안에 들어
// 다운스케일 없이 원해상도. 타일 수가 MAX_TILES 초과(초대형)면 null → 크롭 폴백.
export function tileForVision(img: HTMLImageElement): string[] | null {
  const w = img.naturalWidth, h = img.naturalHeight;
  if (withinBudget(w, h)) return [toPng(img, 0, 0, w, h, VISION_LONG_EDGE)];
  const cols = Math.ceil(w / TILE_TARGET);
  const rows = Math.ceil(h / TILE_TARGET);
  if (cols * rows > MAX_TILES) return null;        // 초대형 → 크롭 모달 폴백
  const cw = Math.ceil(w / cols), ch = Math.ceil(h / rows);
  const tiles: string[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x0 = Math.max(0, c * cw - (cols > 1 ? TILE_OVERLAP : 0));
      const y0 = Math.max(0, r * ch - (rows > 1 ? TILE_OVERLAP : 0));
      const x1 = Math.min(w, (c + 1) * cw + (cols > 1 ? TILE_OVERLAP : 0));
      const y1 = Math.min(h, (r + 1) * ch + (rows > 1 ? TILE_OVERLAP : 0));
      tiles.push(toPng(img, x0, y0, x1 - x0, y1 - y0, VISION_LONG_EDGE));
    }
  }
  return tiles;
}

export async function prepareImage(file: File): Promise<Prepared> {
  let blob: Blob = file;
  if (isHeic(file)) {
    try { blob = await heicToJpeg(file); }
    catch { throw new Error('HEIC 변환에 실패했어요 — jpg/png로 저장해 다시 시도해주세요.'); }
  } else if (!ACCEPTED_MIME.includes(file.type)) {
    throw new Error('지원하지 않는 형식이에요 (PNG·JPEG·WebP·HEIC).');
  }
  if (blob.size > MAX_INPUT_BYTES) throw new Error('이미지가 너무 커요 (8MB 이하로 첨부해주세요).');
  const rawDataUrl = await blobToDataUrl(blob);
  const img = await loadImage(rawDataUrl);
  const tiles = tileForVision(img);
  if (tiles === null) return { kind: 'needsCrop', rawDataUrl };  // 초대형 → 크롭 폴백
  return { kind: 'ready', dataUrls: tiles };
}

// paste/drop 의 DataTransfer 에서 이미지 File 추출.
export function imagesFromDataTransfer(dt: DataTransfer | null): File[] {
  if (!dt) return [];
  const ok = (f: File | null): f is File =>
    !!f && (/^image\//.test(f.type) || /\.hei[cf]$/i.test(f.name));
  const out: File[] = [];
  for (const it of Array.from(dt.items ?? [])) {
    if (it.kind === 'file') { const f = it.getAsFile(); if (ok(f)) out.push(f); }
  }
  if (out.length === 0) for (const f of Array.from(dt.files ?? [])) if (ok(f)) out.push(f);
  return out;
}
