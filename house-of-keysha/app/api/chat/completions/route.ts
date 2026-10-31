import { NextRequest, NextResponse } from 'next/server';
import { generateMaxineReply } from '@/lib/ai/reply-beast';
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
function stableSessionKey(body: any, messages: any[]): string {
  if (body.user) return String(body.user);
  if (body.session_id) return String(body.session_id);
  const first = messages.find((m: any) => m.role === 'user')?.content || '';
  let h = 0; for (let i = 0; i < first.length; i++) h = (h * 31 + first.charCodeAt(i)) | 0;
  const fingerprint = first.slice(0, 4) + first.length;
  return `anon-${Math.abs(h).toString(36)}-${fingerprint.replace(/\W/g, '')}`;
}
export async function POST(req: NextRequest) {
  const secret = process.env.MAXINE_SECRET;
  if (secret) {
    const auth = req.headers.get('authorization') || '';
    if (auth !== `Bearer ${secret}`) return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }
  const body = await req.json();
  const messages = Array.isArray(body.messages) ? body.messages : [];
  const sessionKey = stableSessionKey(body, messages);
  try {
    const { text, provider } = await generateMaxineReply({ sessionKey, messages });
    return NextResponse.json({ id: `chatcmpl-${Date.now()}`, object: 'chat.completion', created: Math.floor(Date.now() / 1000), model: 'maxine', choices: [{ index: 0, message: { role: 'assistant', content: text }, finish_reason: 'stop' }], usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 }, provider });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
