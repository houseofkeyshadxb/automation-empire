import { NextRequest, NextResponse } from 'next/server';
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export async function POST(req: NextRequest, { params }: { params: { provider: string } }) {
  return NextResponse.json({ ok: false, reason: 'handler_not_configured', provider: params.provider }, { status: 501 });
}
