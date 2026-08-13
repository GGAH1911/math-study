// 필기 문서 포맷 — **읽기는 v1·v2·v3 전부, 쓰기는 v3.**
//
// ★왜 v3 인가: 두 기기가 오프라인으로 각각 필기하면 합칠 방법이 있어야 한다. 지금 v2 는
//   스트로크에 **정체성이 없다**(배열의 위치가 곧 신원). 그래서 합칠 때 "이 획과 저 획이
//   같은 것인가" 를 물을 수가 없고, 삭제는 **흔적조차 남지 않아** 한쪽의 지우개질이 다른 쪽의
//   합류로 조용히 되살아난다.
//   → 스트로크에 **id**, 삭제에 **묘비(tombstone)** 를 준다. 그러면 합치기가
//     "id 합집합에서 묘비를 뺀다" 로 끝난다.
//
// ★하위호환은 한 방향이 아니다. **읽기**는 옛 문서를 그대로 읽어야 하고(사장님 필기가 이미 있다),
//   **쓰기**는 v3 로만 한다. 옛 클라이언트가 v3 를 만나면 hydration 을 건너뛸 뿐 로컬 작업을
//   덮어쓰지 않는다 — 동기화가 안 될 뿐 데이터를 잃지 않는다.

export interface InkPoint { x: number; y: number; p?: number }
export interface InkStroke {
  /** v3 에서 부여. 기기 간 병합의 유일한 신원. */
  id: string;
  pts: InkPoint[];
  tool?: string; color?: string; width?: number; dashed?: boolean; pressure?: boolean;
  [k: string]: unknown;
}
export interface InkLayer {
  id: string; name: string; visible: boolean;
  /** 레이어 묘비 — 지운 레이어를 **지우지 않고 표시**한다(합류한 기기가 되살리지 못하게). */
  deleted?: boolean;
}
export interface InkDoc {
  v: 3;
  layers: InkLayer[];
  strokes: Record<string, InkStroke[]>;
  /** 지워진 스트로크 id 묘비. 합칠 때 id 합집합에서 이걸 뺀다. */
  deletedStrokes: string[];
  activeId?: string;
}

export const INK_DOC_VERSION = 3 as const;

/**
 * 스트로크 id 생성. 시간+난수 — 두 기기가 동시에 만들어도 부딪히지 않게.
 *
 * ⚠️ 마이그레이션에서는 이걸 쓰지 않는다. 옛 스트로크는 **내용에서** id 를 만들어야
 *    같은 문서를 두 기기가 각자 변환해도 같은 id 가 나온다(안 그러면 같은 획이 둘로 늘어난다).
 */
export function newStrokeId(): string {
  return `s_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
}

/**
 * 내용 기반 결정적 id — 마이그레이션 전용.
 *
 * ★두 기기가 같은 v2 문서를 각자 v3 로 올려도 **같은 id** 가 나와야 한다. 난수를 쓰면
 *   합류하는 순간 모든 획이 두 벌이 된다. 그래서 좌표·도구·색을 해싱한다.
 *   `layerId`·`index` 를 섞는 이유는 완전히 같은 획을 두 번 그은 경우를 가르기 위해서다.
 */
export function deterministicStrokeId(stroke: Record<string, unknown>, layerId: string, index: number): string {
  const pts = (stroke.pts as InkPoint[] | undefined) ?? [];
  // 좌표를 소수 2자리로 깎아 부동소수 표현 차이가 id 를 가르지 않게 한다.
  const shape = pts.map((p) => `${p.x.toFixed(2)},${p.y.toFixed(2)}`).join(';');
  const src = `${layerId}#${index}#${stroke.tool ?? ''}#${stroke.color ?? ''}#${stroke.width ?? ''}#${shape}`;
  // FNV-1a 32bit ×2(오프셋 다르게) — 브라우저·노드 어디서나 같은 값이 나오는 순수 계산.
  const fnv = (seed: number) => {
    let h = seed >>> 0;
    for (let i = 0; i < src.length; i++) { h ^= src.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    return h.toString(36).padStart(7, '0');
  };
  return `m_${fnv(0x811c9dc5)}${fnv(0x9e3779b9)}`;
}

/**
 * 어떤 버전이 오든 v3 로 정규화해 돌려준다. 못 읽으면 null(호출측이 로컬을 지키게).
 *
 * - v1: 스트로크 배열 하나 → 레이어 L1
 * - v2: `{v:2, layers, strokes, activeId}` → id·묘비 채움
 * - v3: 그대로(빠진 필드만 보정)
 */
export function normalizeInkDoc(raw: unknown): InkDoc | null {
  if (!raw) return null;

  // v1 — 스트로크 배열 하나뿐이던 시절.
  if (Array.isArray(raw)) {
    return withIds({ v: 3, layers: [{ id: 'L1', name: '레이어 1', visible: true }],
                     strokes: { L1: raw as InkStroke[] }, deletedStrokes: [], activeId: 'L1' });
  }
  const d = raw as Record<string, unknown>;
  if (!Array.isArray(d.layers) || typeof d.strokes !== 'object' || d.strokes === null) return null;

  const layers = (d.layers as InkLayer[]).filter((l) => l && typeof l.id === 'string');
  if (layers.length === 0) return null;
  const strokes: Record<string, InkStroke[]> = {};
  for (const l of layers) strokes[l.id] = ((d.strokes as Record<string, InkStroke[]>)[l.id] ?? []).filter(Boolean);

  const doc: InkDoc = {
    v: 3, layers, strokes,
    deletedStrokes: Array.isArray(d.deletedStrokes) ? (d.deletedStrokes as string[]).filter((s) => typeof s === 'string') : [],
    activeId: typeof d.activeId === 'string' ? d.activeId : layers[0].id,
  };
  return withIds(doc);
}

/** id 없는 스트로크에 결정적 id 를 채운다(이미 있으면 건드리지 않는다). */
function withIds(doc: InkDoc): InkDoc {
  for (const l of doc.layers) {
    const arr = doc.strokes[l.id] ?? [];
    doc.strokes[l.id] = arr.map((s, i) =>
      (s && typeof s.id === 'string' && s.id) ? s : { ...s, id: deterministicStrokeId(s as never, l.id, i) });
  }
  return doc;
}

/** 보이는 스트로크만 — 묘비에 오른 것은 뺀다. 렌더·내보내기가 쓰는 진입점. */
export function visibleStrokes(doc: InkDoc, layerId: string): InkStroke[] {
  if (doc.deletedStrokes.length === 0) return doc.strokes[layerId] ?? [];
  const dead = new Set(doc.deletedStrokes);
  return (doc.strokes[layerId] ?? []).filter((s) => !dead.has(s.id));
}
