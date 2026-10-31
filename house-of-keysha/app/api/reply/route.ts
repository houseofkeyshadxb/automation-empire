import { NextRequest, NextResponse } from 'next/server';
import { generateMaxineReply } from '@/lib/ai/reply-beast';

export const runtime = 'nodejs';

export async function POST(req: NextRequest) {
  try {
    const { sessionKey, messages } = await req.json();

    if (!sessionKey || !messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Missing required fields: sessionKey, messages' },
        { status: 400 }
      );
    }

    const reply = await generateMaxineReply({ sessionKey, messages });

    return NextResponse.json({
      text: reply.text,
      provider: reply.provider,
      sessionKey,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('🚨 /api/reply error:', error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Internal server error',
        fallback: 'I apologize for the technical difficulty. Please try again in a moment.'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Maxine WhatsApp Bot API',
    endpoint: '/api/reply',
    method: 'POST',
    required: ['sessionKey', 'messages']
  });
}
