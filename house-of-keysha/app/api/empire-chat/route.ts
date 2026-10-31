import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { message, persona } = await req.json();
    const apiKey = process.env.GROQ_API_KEY;

    if (!apiKey) {
      return NextResponse.json(
        { error: 'Groq API key not configured' },
        { status: 500 }
      );
    }

    const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: [
          {
            role: 'system',
            content: `You are ${persona || 'Mistress Keysha'} from House of Keysha Empire in Dubai. 
Respond naturally, flirty, with occasional spelling mistakes. Keep responses under 150 words. 
If someone is a time-waster, pivot to paid options. Reference booking refs when appropriate.`
          },
          {
            role: 'user',
            content: message
          }
        ],
        temperature: 0.85,
        max_tokens: 300
      })
    });

    const data = await groqResponse.json();
    const reply = data.choices?.[0]?.message?.content || 'Let me get back to you on that...';

    return NextResponse.json({ 
      response: reply,
      persona: persona || 'Keysha',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Chat error:', error);
    return NextResponse.json(
      { error: 'Chat service temporarily offline' },
      { status: 500 }
    );
  }
}
