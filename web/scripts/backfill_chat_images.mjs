// chat_history 안에 인라인으로 박혀 있는 dataURL 을 chat_images 참조로 옮긴다(1회성 백필).
//
// ★프로덕션과 **같은 모듈**(lib/chat-images.ts)을 그대로 import 한다. 여기서 해시·정규식을
//   복붙하면 그 순간 백필과 런타임이 갈라져, 되돌린 값이 원본과 다른 사고가 난다.
//
// 실행(컨테이너 안 — DB 는 호스트 포트가 없다):
//   docker compose -f deploy/docker-compose.yml exec -T web \
//     node --experimental-strip-types --import ./scripts/ts-resolve-hook.mjs \
//          scripts/backfill_chat_images.mjs [--apply]
// 기본은 dry-run. --apply 를 줘야 쓴다.
import sql from '../src/lib/db.ts';
import { externalizeImages } from '../src/lib/chat-images.ts';

const APPLY = process.argv.includes('--apply');
const rows = await sql`
  SELECT user_id, collection, slug, messages, pg_column_size(messages) AS bytes FROM chat_history
`;
let moved = 0, before = 0, after = 0;
for (const r of rows) {
  const inline = JSON.stringify(r.messages).match(/data:image\/(?:png|jpeg|webp);base64,/g)?.length ?? 0;
  if (inline === 0) { before += Number(r.bytes); after += Number(r.bytes); continue; }
  const stored = APPLY ? await externalizeImages(r.messages) : r.messages;
  const size = APPLY ? JSON.stringify(stored).length : Number(r.bytes);
  if (APPLY) {
    await sql`UPDATE chat_history SET messages = ${sql.json(stored)}
              WHERE user_id = ${r.user_id} AND collection = ${r.collection} AND slug = ${r.slug}`;
  }
  moved += inline; before += Number(r.bytes); after += size;
  console.log(`  ${r.collection}/${r.slug}: 인라인 ${inline}장 · ${(Number(r.bytes) / 1024) | 0}KB → ${(size / 1024) | 0}KB`);
}
console.log(`${APPLY ? '[적용]' : '[dry-run]'} 대화 ${rows.length}건 · 이미지 ${moved}장 · ` +
            `${(before / 1024) | 0}KB → ${(after / 1024) | 0}KB`);
await sql.end();
