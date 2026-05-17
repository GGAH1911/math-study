import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';

export const prerender = false;

const VENV_PYTHON = resolve(process.cwd(), '..', '.venv', 'bin', 'python');
const MAX_OUTPUT = 4096;
const TIMEOUT_MS = 10_000;

const HEADER = `import sympy
from sympy import Symbol, symbols, solve, simplify, expand, factor, diff, integrate, limit, Sum, Product, oo, pi, E, I, sqrt, sin, cos, tan, log, ln, exp, Matrix, Rational, S
x, y, z, n, k, t, a, b, c = symbols('x y z n k t a b c')
`;

type RunRequest = { code: string };

export const POST: APIRoute = async ({ request }) => {
  let body: RunRequest;
  try { body = await request.json(); }
  catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400 }); }

  const code = (body.code ?? '').trim();
  if (!code) return new Response(JSON.stringify({ error: 'empty code' }), { status: 400 });
  if (code.length > 4000) return new Response(JSON.stringify({ error: 'code too long' }), { status: 400 });

  return new Promise<Response>((resolveResp) => {
    const child = spawn(VENV_PYTHON, ['-c', HEADER + code], {
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';
    let truncated = false;
    const onChunk = (s: string) => (chunk: Buffer) => {
      const t = chunk.toString('utf-8');
      if (s === 'out') {
        if (stdout.length + t.length > MAX_OUTPUT) { stdout += t.slice(0, MAX_OUTPUT - stdout.length); truncated = true; }
        else stdout += t;
      } else {
        if (stderr.length + t.length > MAX_OUTPUT) { stderr += t.slice(0, MAX_OUTPUT - stderr.length); truncated = true; }
        else stderr += t;
      }
    };
    child.stdout.on('data', onChunk('out'));
    child.stderr.on('data', onChunk('err'));

    const killer = setTimeout(() => { child.kill('SIGKILL'); }, TIMEOUT_MS);

    child.on('close', (code) => {
      clearTimeout(killer);
      resolveResp(new Response(JSON.stringify({
        ok: code === 0,
        exit_code: code,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        truncated,
      }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
    });
    child.on('error', (e) => {
      clearTimeout(killer);
      resolveResp(new Response(JSON.stringify({ ok: false, error: e.message }), { status: 500 }));
    });
  });
};
