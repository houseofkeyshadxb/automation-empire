import { getDb } from '@/lib/supabase/server';
export type FunnelStage = 'AGE_GATE' | 'DISCOVERY' | 'PERSONA_ALIGNMENT' | 'GRAND_SLAM_OFFER' | 'OBJECTION_HANDLING' | 'CLOSING_SLOT' | 'HUMAN_HANDOFF' | 'CLOSED';
export type PersonaKey = 'becky' | 'mistress_keysha' | 'keysha_seductress' | 'switch_muse';
export interface FunnelContext { stage: FunnelStage; ageVerified: boolean; userDraw?: string; matchedPersona?: PersonaKey; objectionsEncountered: string[]; lastInteractionAt: number; }
export function emptyFunnel(): FunnelContext { return { stage: 'AGE_GATE', ageVerified: false, objectionsEncountered: [], lastInteractionAt: Date.now() }; }
export async function getFunnelStateFromDB(sessionKey: string): Promise<FunnelContext> {
  const { data } = await getDb().from('reply_sessions').select('funnel').eq('session_key', sessionKey).maybeSingle();
  if (data?.funnel) return data.funnel as FunnelContext;
  const fresh = emptyFunnel();
  if (data) { await getDb().from('reply_sessions').update({ funnel: fresh }).eq('session_key', sessionKey); }
  else { await getDb().from('reply_sessions').insert({ session_key: sessionKey, funnel: fresh }); }
  return fresh;
}
export async function saveFunnelState(sessionKey: string, state: FunnelContext): Promise<void> {
  await getDb().from('reply_sessions').upsert({ session_key: sessionKey, funnel: state, updated_at: new Date().toISOString() }, { onConflict: 'session_key' });
}
