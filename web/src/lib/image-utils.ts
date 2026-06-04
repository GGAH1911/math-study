// 클라이언트 전용 — 첨부 이미지 검증·HEIC 변환·리사이즈·크롭.
// window/FileReader/canvas/heic2any(브라우저 API)를 쓰므로 서버에서 import 금지.

export const ACCEPTED_MIME = ['image/png', 'image/jpeg', 'image/webp'];
export const MAX_INPUT_BYTES = 8 * 1024 * 1024;   // 입력 원본 상한
export const VISION_LONG_EDGE = 1568;             // Claude vision 권장 긴 변
const CROP_LONG_EDGE = 2200;                      // 긴 변이 이보다 길면 크롭 모달
const CROP_AREA = 2_400_000;                      // 면적이 이보다 크면(아이패드 등) 크롭 모달

export type Prepared =
  | { kind: 'ready'; dataUrl: string }            // 1568 PNG 완료 → 바로 첨부
  | { kind: 'needsCrop'; rawDataUrl: string };    // 너무 큼 → 크롭 모달로

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
  const long = Math.max(img.naturalWidth, img.naturalHeight);
  const area = img.naturalWidth * img.naturalHeight;
  if (long > CROP_LONG_EDGE || area > CROP_AREA) return { kind: 'needsCrop', rawDataUrl };
  return { kind: 'ready', dataUrl: downscaleFull(img) };
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
