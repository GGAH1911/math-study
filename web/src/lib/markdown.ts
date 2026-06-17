// 공유 markdown helper — ChatPanel 및 학습 노트 흐름이 사용.
// 핵심 기능: 표(table) 파싱. inline·escape는 호출자가 자체 보유한 것 사용.
//
// 표를 별도 라이브러리 없이 처리하는 이유:
//  - remark-gfm은 200KB+ 번들 + AST 파이프라인 통합 비용 큼.
//  - 표 외 markdown 처리는 이미 자체 구현이 있음.
//  - parser 자체는 50줄 이하로 충분.

/**
 * 표 detect 후 HTML로 변환. 표 아니면 null.
 *
 * 표 grammar (GFM 호환 최소 spec):
 *   |  H1  |  H2  |   ← 첫 줄 (헤더)
 *   |------|------|   ← 둘째 줄 (alignment / separator)
 *   |  a   |  b   |   ← 0개 이상 body 행
 *
 * 각 셀 텍스트는 `cellTransform` 콜백으로 가공 (보통 escape + inline markdown).
 * KaTeX `$...$` 는 그대로 두고 호출자의 KaTeX 단계에서 처리.
 *
 * @param lines 줄 단위로 자른 block (paragraph 내부)
 * @param cellTransform 셀 텍스트 → HTML 변환기
 * @returns 표 HTML 문자열, 또는 null (표 아님)
 */
export function parseTableBlock(
  lines: string[],
  cellTransform: (cell: string) => string,
): string | null {
  if (lines.length < 2) return null;
  const isRowLine = (s: string) => /^\s*\|.+\|\s*$/.test(s);
  const isAlignLine = (s: string) => /^\s*\|[\s\-:|]+\|\s*$/.test(s) && /-/.test(s);
  if (!isRowLine(lines[0]) || !isAlignLine(lines[1])) return null;
  // body는 isRowLine을 만족하는 동안 계속 — 첫 비-row 만나면 stop.
  // 일반적으로 paragraph block 단위로 들어오므로 body가 paragraph 끝까지 이어짐.
  const bodyLines: string[] = [];
  for (let i = 2; i < lines.length; i++) {
    if (!isRowLine(lines[i])) return null; // 표 도중 잡 텍스트 — 표 아님으로 reject
    bodyLines.push(lines[i]);
  }
  const splitCells = (raw: string): string[] => {
    // 앞뒤 `|` 제거, `\|`는 placeholder로 보호 후 split.
    const PH = '';
    const inner = raw.trim().replace(/^\||\|$/g, '').replace(/\\\|/g, PH);
    return inner.split('|').map((c) => c.replace(new RegExp(PH, 'g'), '|').trim());
  };
  const head = splitCells(lines[0]).map((c) => `<th>${cellTransform(c)}</th>`).join('');
  const body = bodyLines
    .map((row) => '<tr>' + splitCells(row).map((c) => `<td>${cellTransform(c)}</td>`).join('') + '</tr>')
    .join('');
  return `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

/**
 * `parseTableBlock`을 paragraph 단위로 호출하는 편의 함수.
 * paragraph 텍스트가 표면 HTML 반환, 아니면 null.
 */
export function tryParseTable(
  paragraph: string,
  cellTransform: (cell: string) => string,
): string | null {
  const lines = paragraph.split('\n').filter((l) => l.trim().length > 0);
  // 박스드로잉(┌─┐ │ ├┤ └─┘ 등) ASCII-아트 표 → 마크다운 표로 정규화 후 파싱.
  // (마크다운 파이프 표는 박스문자가 없어 이 경로를 안 타고 기존 parseTableBlock 그대로 → 무회귀.)
  if (/[┌┐└┘├┤┬┴┼─━│┃]/.test(paragraph)) {
    const content = lines
      .map((l) => l.replace(/[│┃]/g, '|').trim())            // 세로 박스선 → 파이프
      .map((l) => l.replace(/\|\s+\|\s*$/, '|'))              // 박스 프레임이 만든 맨끝 빈 셀 제거
      .filter((l) => l.includes('|') && /[0-9A-Za-z가-힣√π°∞]/.test(l)); // 셀 내용 있는 행만(테두리·구분선 제거)
    if (content.length >= 2 && /^\|.*\|$/.test(content[0])) {
      const cols = content[0].replace(/^\||\|$/g, '').split('|').length;
      const align = '|' + Array(cols).fill('---').join('|') + '|';
      const html = parseTableBlock([content[0], align, ...content.slice(1)], cellTransform);
      if (html) return html;
    }
  }
  return parseTableBlock(lines, cellTransform);
}
