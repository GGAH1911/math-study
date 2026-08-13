// 대화 첨부 이미지의 **내용주소 참조 계층**.
//
// 저장할 때 dataURL → 'img:sha256:<hex>' 로 바꿔 본문은 chat_images 에 1부만 두고,
// 읽을 때 되돌린다. chat_history.messages 는 매 턴 통째로 재기록되므로, 이미지가 그 안에
// 있으면 턴당 쓰기가 첨부 총량만큼 든다 — 그걸 끊는 게 목적이다.
//
// ★백엔드(지금은 postgres bytea)는 나중에 R2 로 갈아끼운다. 참조 형식과 이 모듈의
//   외부 인터페이스는 그대로 두는 게 설계 의도다 — 호출측이 저장소를 몰라야 교체가 싸다.
import { createHash } from 'node:crypto';
import sql from './db.ts';

const REF_PREFIX = 'img:sha256:';
const DATA_URL_RE = /^data:(image\/(?:png|jpeg|webp));base64,([A-Za-z0-9+/=]+)$/;
const MAX_IMAGE_BYTES = 6 * 1024 * 1024;   // 1장 상한 — 타일은 보통 200KB 안쪽

export const isImageRef = (s: unknown): s is string =>
  typeof s === 'string' && s.startsWith(REF_PREFIX);

/** 메시지 배열 안의 이미지 자리(images[] · displayImage)를 훑어 콜백을 적용한다. */
function mapImageFields(messages: unknown[], fn: (v: string) => string): unknown[] {
  return messages.map((m) => {
    if (!m || typeof m !== 'object') return m;
    const msg = m as Record<string, unknown>;
    if (!Array.isArray(msg.images) && typeof msg.displayImage !== 'string') return m;
    const out: Record<string, unknown> = { ...msg };
    if (Array.isArray(msg.images)) {
      out.images = msg.images.map((v) => (typeof v === 'string' ? fn(v) : v));
    }
    if (typeof msg.displayImage === 'string') out.displayImage = fn(msg.displayImage);
    return out;
  });
}

/**
 * dataURL → 참조. 본문은 chat_images 에 upsert(중복이면 그냥 둔다).
 *
 * ★이미 참조인 값·인식 못 할 값은 **손대지 않고 그대로 통과**시킨다. 저장은 매 턴 전체
 *   배열로 들어오므로 같은 메시지가 반복해서 지나가고, 그때 참조를 다시 해석하려 들면
 *   원본을 잃는다.
 */
export async function externalizeImages(messages: unknown[]): Promise<unknown[]> {
  const blobs = new Map<string, { mime: string; buf: Buffer }>();
  const mapped = mapImageFields(messages, (v) => {
    const m = DATA_URL_RE.exec(v);
    if (!m) return v;                                  // 참조이거나 알 수 없는 형식 → 보존
    const buf = Buffer.from(m[2], 'base64');
    if (buf.byteLength > MAX_IMAGE_BYTES) return v;     // 과대 → 인라인 유지(상한은 POST 가 잡는다)
    const hash = createHash('sha256').update(buf).digest('hex');
    blobs.set(hash, { mime: m[1], buf });
    return REF_PREFIX + hash;
  });
  for (const [hash, { mime, buf }] of blobs) {
    await sql`
      INSERT INTO chat_images (hash, mime, data, bytes) VALUES (${hash}, ${mime}, ${buf}, ${buf.byteLength})
      ON CONFLICT (hash) DO NOTHING
    `;
  }
  return mapped;
}

/**
 * 참조 → dataURL. 클라이언트 계약을 그대로 유지하기 위해 읽을 때 되돌린다.
 *
 * ⚠️ 본문이 없는 참조(수동 정리·GC 사고)는 **빈 문자열이 아니라 참조 그대로** 남긴다.
 *    빈 값으로 바꾸면 다음 저장 때 그 상태가 굳어 복구 불능이 된다.
 */
export async function inflateImages(messages: unknown[]): Promise<unknown[]> {
  const refs = new Set<string>();
  mapImageFields(messages, (v) => { if (isImageRef(v)) refs.add(v.slice(REF_PREFIX.length)); return v; });
  if (refs.size === 0) return messages;
  const rows = await sql<{ hash: string; mime: string; data: Buffer }[]>`
    SELECT hash, mime, data FROM chat_images WHERE hash = ANY(${[...refs]})
  `;
  const byHash = new Map(rows.map((r) => [r.hash, `data:${r.mime};base64,${r.data.toString('base64')}`]));
  return mapImageFields(messages, (v) =>
    isImageRef(v) ? (byHash.get(v.slice(REF_PREFIX.length)) ?? v) : v);
}

/**
 * 어떤 대화에서도 더는 참조되지 않는 본문을 지운다.
 *
 * ★messages 안 **문자열**이 참조라 FK 를 걸 수 없다 → 탈퇴·대화 삭제 뒤에 이걸 부른다.
 *   `LIKE '%'||hash||'%'` 는 인덱스를 못 타지만, 이 테이블은 대화 수만큼만 크고
 *   호출도 탈퇴 시점에나 일어난다.
 */
export async function gcOrphanImages(): Promise<number> {
  const rows = await sql<{ n: string }[]>`
    WITH refd AS (
      SELECT DISTINCT t.m[1] AS hash
      FROM chat_history c,
           LATERAL regexp_matches(c.messages::text, 'img:sha256:([0-9a-f]{64})', 'g') AS t(m)
    )
    DELETE FROM chat_images ci WHERE NOT EXISTS (SELECT 1 FROM refd r WHERE r.hash = ci.hash)
    RETURNING 1 AS n
  `;
  return rows.length;
}
