import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import matter from 'gray-matter';

export const prerender = false;

const WEB_ROOT = process.cwd();
const DOCS = resolve(WEB_ROOT, '..', 'docs', 'concepts');

const TUTOR_SYSTEM = `당신은 한국 수능을 준비하는 학생용 수학 wiki의 콘텐츠 라이터입니다.
한 번에 spoke 페이지(정의/정리/예제) 하나의 '본문' 섹션을 작성합니다.

요구사항:
1. 한국어로. 한국 고등학교 교육과정 용어 우선.
2. 수식은 KaTeX inline \`$...$\` 또는 display \`$$...$$\`로.
3. 200-400 단어 분량.
4. 구조:
   - 정의(definition): ### 정확한 진술 → ### 직관/기하적 의미 → ### 한 줄 예
   - 정리(theorem): ### 진술 + 가정 → ### 간단한 유도/증명 스케치 → ### 의의/응용
   - 예제(example): ### 문제 → ### 단계별 풀이 → ### 답 → ### 변형/주의
5. h1, h2 헤더 절대 사용 금지. h3(###) 이하만.
6. 검산 가능한 수치 예제는 sympy 코드 한 줄 포함 가능.
7. 출력은 본문 마크다운만. "본문:" 같은 라벨 금지. ### 헤더로 시작.`;

type RegenerateRequest = {
  slug: string;
  model?: 'haiku' | 'sonnet';
};

function fmField(text: string, key: string): string {
  const m = text.match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
  return m ? m[1].trim() : '';
}

function listField(text: string, key: string): string[] {
  const m = text.match(new RegExp(`^${key}:\\s*\\[(.*?)\\]`, 'm'));
  if (!m || !m[1].trim()) return [];
  return m[1].split(',').map((s) => s.trim()).filter(Boolean);
}

export const POST: APIRoute = async ({ request }) => {
  const { slug, model = 'haiku' } = (await request.json()) as RegenerateRequest;
  // sub-dir slug 허용. `..` 와 backslash 차단.
  if (!slug || /\\|\.\./.test(slug) || !/^[\w가-힣/-]+$/.test(slug)) {
    return new Response(JSON.stringify({ error: 'invalid slug' }), { status: 400 });
  }
  const file = resolve(DOCS, `${slug}.md`);
  if (!file.startsWith(resolve(DOCS) + '/')) {
    return new Response(JSON.stringify({ error: 'path escape' }), { status: 400 });
  }
  let text: string;
  try {
    text = readFileSync(file, 'utf-8');
  } catch {
    return new Response(JSON.stringify({ error: 'spoke not found' }), { status: 404 });
  }

  const parsed = matter(text);
  const ctype = (parsed.data.concept_type as string) ?? '';
  if (ctype === 'unit') {
    return new Response(JSON.stringify({ error: 'unit pages do not regenerate' }), { status: 400 });
  }

  const grade = fmField(text, 'grade');
  const unit = fmField(text, 'unit');
  const prereqs = listField(text, 'prerequisites');
  const briefMatch = text.match(/## 요약\s*\n([^\n#]+)/);
  const brief = briefMatch ? briefMatch[1].trim() : '';
  const preLabels = prereqs.map((p) => p.split('/').pop()?.replace(/\.md$/, '').replace(/_/g, ' ')).join(', ') || '없음';

  const userPrompt = `다음 spoke 페이지의 본문을 작성하세요.

페이지 slug: ${slug}
타입: ${ctype}
학년: ${grade}
소속 단원: ${unit}
선수 개념: ${preLabels}
페이지 요약(1줄): ${brief}

이 spoke를 처음 보는 학생에게 친절하면서도 정확하게 설명해 주세요. h3(###) 이하 헤더만. 출력은 markdown 본문만.`;

  return new Promise<Response>((resolveResp) => {
    const child = spawn('claude', [
      '-p',
      '--model', model,
      '--max-turns', '1',
      '--output-format', 'text',
      '--no-session-persistence',
      '--system-prompt', TUTOR_SYSTEM,
      userPrompt,
    ], { env: process.env });

    let buf = '';
    child.stdout.on('data', (c) => { buf += c.toString('utf-8'); });
    let err = '';
    child.stderr.on('data', (c) => { err += c.toString('utf-8'); });

    child.on('close', (code) => {
      if (code !== 0 || !buf.trim()) {
        resolveResp(new Response(JSON.stringify({ error: 'claude failed', stderr: err.slice(0, 500) }), { status: 500 }));
        return;
      }
      let body = buf.trim();
      // Drop accidental h1/h2 prefix
      body = body.replace(/^\s*#{1,2}\s+[^\n]+\n+/, '');

      // Splice into the spoke file
      const splicePattern = /(## 본문[^\n]*\n)([\s\S]*?)(\n## )/;
      let newText: string;
      if (splicePattern.test(text)) {
        newText = text.replace(splicePattern, (_, h, _old, tail) => `${h}\n${body}\n${tail}`);
      } else {
        const checkIdx = text.indexOf('## 학습 체크');
        if (checkIdx >= 0) {
          newText = text.slice(0, checkIdx) + '## 본문\n\n' + body + '\n\n' + text.slice(checkIdx);
        } else {
          newText = text.trimEnd() + '\n\n## 본문\n\n' + body + '\n';
        }
      }
      // Mark auto_explained: true
      if (/^auto_explained:/m.test(newText)) {
        newText = newText.replace(/^auto_explained:.*$/m, 'auto_explained: true');
      } else {
        newText = newText.replace(/^(updated:.*)$/m, '$1\nauto_explained: true');
      }
      try {
        writeFileSync(file, newText, 'utf-8');
      } catch (e) {
        resolveResp(new Response(JSON.stringify({ error: 'write failed', message: (e as Error).message }), { status: 500 }));
        return;
      }
      resolveResp(new Response(JSON.stringify({ ok: true, slug, length: body.length }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }));
    });

    child.on('error', (e) => {
      resolveResp(new Response(JSON.stringify({ error: 'spawn failed', message: e.message }), { status: 500 }));
    });
  });
};
