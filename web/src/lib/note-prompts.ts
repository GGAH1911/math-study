// Client-safe prompt strings for the "학습 노트" UX. Shared between
// LearningNoteButton (initial request) and ChatPanel (followup action
// buttons: 더 짧게 / 더 자세히 / 핵심만).
//
// The leading `[학습 노트 요청]` marker lets the chat UI recognize a
// note-request message and surface the action row beneath the assistant's
// reply. Mirror of the existing `[자동 계산 결과]` etc. marker convention.

export const NOTE_MARKER = '[학습 노트 요청]';

export function buildNoteUserPrompt(unitTitle: string): string {
  return `${NOTE_MARKER} "${unitTitle}" 페이지에서 지금까지 한 대화를 정리해 학습 노트를 작성해줘.

다음 4섹션 markdown으로:

## ✅ 핵심 정리
- (2~4 bullets) 핵심 정의·공식. 수식은 \`$...$\` KaTeX.

## 🤔 헷갈렸던 부분
- (선택) 학생이 막혔던 step과 어떻게 풀렸는지. 없으면 생략.

## 🔁 다시 봐야 할 부분
- (1~2 bullets) 복습 포인트.

## ➡️ 다음 학습
- (1~2 bullets) 선수/enables 활용. 마크다운 링크 \`[name](/concepts/<slug>)\` 형식.

3분이면 다시 떠올릴 수 있는 길이로 (6~12줄). 답변은 \`## ✅\` 부터 시작.`;
}

// Followup prompts for the action row under a note response. Each keeps
// the `[학습 노트 요청]` marker so the action row reappears on the next
// reply — letting the student iterate "더 짧게" → "더 자세히" → 저장.
export const NOTE_FOLLOWUPS = {
  shorter: `${NOTE_MARKER} 위 노트를 절반 길이로 다시 정리해줘. 같은 4섹션 구조는 유지.`,
  longer:  `${NOTE_MARKER} 위 노트에 직관 설명과 예시를 1~2개 더 추가해줘. 같은 4섹션은 유지.`,
  coreOnly: `${NOTE_MARKER} 위 노트에서 정의·공식 부분만 한 줄씩으로 압축해줘. 다른 섹션은 생략.`,
} as const;

export type NoteFollowup = keyof typeof NOTE_FOLLOWUPS;

// Detect whether a user message is a note request — used to flag the
// following assistant message for the action row.
export function isNoteRequest(content: string): boolean {
  return content.startsWith(NOTE_MARKER);
}
