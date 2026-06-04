// 모델이 vision(이미지 입력)을 지원하지 않는지 판정.
// openrouter.ts 의 인라인 정규식을 추출해 서버·클라이언트가 공유한다.
// 패턴: :free 티어, nemotron, deepseek-v*-flash/chat, gemma2 이하, qwen2.5(비 -vl).
export function isVisionDisabled(model: string): boolean {
  return /:free($|\b)|nemotron|deepseek-v[0-9]+-flash|deepseek-chat/i.test(model)
    || (/gemma/i.test(model) && !/gemma[34]/i.test(model))
    || /qwen2\.5(?!-vl)/i.test(model);
}
