// 학습 상태 변경을 **정본 이벤트**로 남긴다. 파생 상태(problem_state·concept_mastery)는
// 이 기록으로부터 다시 만들 수 있어야 한다.
//
// ★지금은 이벤트와 파생 상태를 **같은 트랜잭션에서 함께** 쓴다(dual-write). 재계산기가
//   들어오기 전까지 파생 상태가 여전히 읽기 경로이기 때문이다. 트랜잭션을 나누면
//   "이벤트는 남았는데 화면은 그대로" 또는 그 반대가 생기고, 그게 정확히 재계산이 못 고치는
//   불일치다.
// ★`Sql` 이 아니라 `ISql` 이다. postgres.js 에서 `Sql`(풀 클라이언트)과
//   `TransactionSql`(sql.begin 이 넘겨주는 핸들)은 **형제** 이고 둘 다 `ISql` 을 확장한다
//   — `TransactionSql` 은 `Sql` 의 하위 타입이 «아니다»(CLOSE·END·options·begin 등이 없다).
//   그래서 매개변수를 `Sql` 로 잡으면 트랜잭션 안에서 부르는 호출부가 전부 ts(2345) 로 깨진다.
//   이 함수가 실제로 쓰는 것은 태그드 템플릿 호출 하나뿐이고, 그건 `ISql` 에 있다.
import type { ISql } from 'postgres';
import sql from './db.ts';

export const EVENT_KINDS = [
  'problem.reset',           // 문제 학습 상태 초기화(파생 상태 DELETE)
  'problem.mark_mastered',   // 사용자가 "다 안다" 고 선언
  'problem.skip',            // 사용자가 미룸
  'concept.mastery_promote', // 개념 숙련도 승급 — payload.evidence 는 재계산으로 복원 불가
] as const;
export type EventKind = (typeof EVENT_KINDS)[number];

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export interface RecordEventInput {
  userId: string;
  kind: EventKind;
  target: string;
  payload?: Record<string, unknown>;
  /** 클라이언트 생성 멱등키. 오프라인 큐 재전송이 중복으로 남지 않게 한다. */
  eventId?: string;
  /** 기기에서 일어난 시각. 오프라인 합류 시 서버 수신 시각과 크게 벌어진다. */
  occurredAt?: string;
}

/**
 * 이벤트 1건 기록. 같은 `eventId` 가 이미 있으면 **아무것도 하지 않는다**(멱등).
 *
 * @returns 새로 기록됐으면 seq, 이미 있던 이벤트면 null
 */
export async function recordEvent(
  input: RecordEventInput,
  tx: ISql = sql,
): Promise<number | null> {
  const { userId, kind, target, payload = {}, eventId, occurredAt } = input;
  // ★신뢰하지 않는 값이 그대로 들어오면 kind 오타가 조용히 저장돼 재계산에서 통째로 누락된다.
  if (!EVENT_KINDS.includes(kind)) throw new Error(`unknown event kind: ${kind}`);
  const id = eventId && UUID_RE.test(eventId) ? eventId : null;
  // 기기 시각은 못 믿는다 — 파싱 실패나 미래 시각이면 서버 시각으로 떨어뜨린다.
  const at = occurredAt && !Number.isNaN(Date.parse(occurredAt))
    ? new Date(Math.min(Date.parse(occurredAt), Date.now())).toISOString()
    : null;

  const rows = await tx<{ seq: string }[]>`
    INSERT INTO learning_events (event_id, user_id, kind, target, payload, occurred_at)
    VALUES (
      ${id ?? sql`gen_random_uuid()`}, ${userId}, ${kind}, ${target},
      ${sql.json(payload as never)}, ${at ?? sql`NOW()`}
    )
    ON CONFLICT (user_id, event_id) DO NOTHING
    RETURNING seq
  `;
  return rows[0] ? Number(rows[0].seq) : null;
}
