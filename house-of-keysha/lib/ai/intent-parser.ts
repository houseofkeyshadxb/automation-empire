import type { FunnelContext, PersonaKey } from './funnel-state';

const HUMAN_INTENT = /\b(human|real person|manager|speak to someone|call me|complain|supervisor)\b/i;
const PRICE_OBJ    = /\b(cheaper|discount|expensive|too much|afford|budget|reduce|costly|steep)\b/i;
const CLOSE_INTENT = /\b(book|reserve|slot|screening|deposit|confirm|tonight|tomorrow|when can|let'?s do it|i'?m in)\b/i;

// D-001/D-003: explicit wrong-number / spam. NOTE: no /^.{0,3}$/ — that killed "hi".
const NOT_CUSTOMER = /\b(wrong (number|person)|number (wrong|sorry)|sorry wrong|accident(al)?|deliver(y)?|parcel|courier|your order|food delivery|package|job offer|hiring|resume|cv|job application|interview|seo|marketing agency|grow your|promote your|crypto|investment opportunity|forex|trading signals|loan offer|credit card|insurance offer)\b/i;

// D-005: positive business intent — must start the funnel even on msg 1
const CUSTOMER_INTENT = /\b(book|booking|price|pricing|cost|rate|rates|service|services|available|availability|session|sessions|massage|companion|companionship|hire|appointment|slot|menu|offer|treatment|how much)\b/i;

// D-004: bare greeting — keep funnel OPEN, do not pitch, do not close
const CASUAL = /^(hi+|hey+|hello+|yo|sup|hiya|howdy|good (morning|afternoon|evening)|what'?s up|wsg|salam|marhaba)[.!\s]*$/i;

// D-006: robust age confirmation
const AGE_UNDER = /\b(i'?m\s*(?:1[0-9]|20)\b|i\s+am\s*(?:1[0-9]|20)\b|under\s*2[01]|not\s+yet|too\s+young|below\s*21|minor)\b/i;
const AGE_YES   = /\b(21\+?|2[1-9]|[3-9]\d|adult|yes|yeah|yep|confirm|agree|affirmative|sure|ok|okay)\b/i;

function detectPersona(t: string): PersonaKey | undefined {
  const s = t.toLowerCase();
  if (/\b(becky|submissive|in control|lead|boss|in charge)\b/.test(s)) return 'becky';
  if (/\b(keysha|mistress|let go|controlled|submit|surrender)\b/.test(s)) return 'mistress_keysha';
  if (/\b(both|switch|dual)\b/.test(s)) return 'switch_muse';
  if (/\b(pepper|hotwife|mommy|goddess|seductress|tease)\b/.test(s)) return 'keysha_seductress';
  return undefined;
}

export function evaluateNextStage(cur: FunnelContext, text: string): FunnelContext {
  const t = text.toLowerCase().trim();
  const next: FunnelContext = { ...cur, objectionsEncountered: [...cur.objectionsEncountered], lastInteractionAt: Date.now() };
  if (!t) return next;

  // Human intent anywhere → handoff
  if (HUMAN_INTENT.test(t)) { next.stage = 'HUMAN_HANDOFF'; return next; }

  if (cur.stage === 'CLOSED' && CUSTOMER_INTENT.test(t)) {
    next.stage = 'AGE_GATE'; next.ageVerified = false; return next;
  }

  // D-003: spam check applies at every stage, not just AGE_GATE
  if (NOT_CUSTOMER.test(t)) { next.stage = 'CLOSED'; return next; }

  // ── AGE_GATE — the tricky entry point ──
  if (cur.stage === 'AGE_GATE' && !cur.ageVerified) {
    // D-004: bare greeting → stay open, Maxine will reply "Hey 💫", wait
    if (CASUAL.test(t)) return next;

    // D-005: business signal on first message → ask age
    if (CUSTOMER_INTENT.test(t)) {
      if (!next.userDraw) next.userDraw = text.slice(0, 300);
      return next;
    }

    // Age confirmation (in case they answered our age question)
    if (AGE_UNDER.test(t)) { next.stage = 'HUMAN_HANDOFF'; return next; }
    if (AGE_YES.test(t)) {
      next.ageVerified = true;
      next.stage = 'DISCOVERY';
      return next;
    }

    // No signal, not greeting, not age → give one grace turn, then close on the next
    if (t.length > 40) { next.stage = 'CLOSED'; return next; }
    return next;
  }

  switch (cur.stage) {
    case 'AGE_GATE': {
      if (AGE_UNDER.test(t)) next.stage = 'HUMAN_HANDOFF';
      else if (AGE_YES.test(t)) { next.ageVerified = true; next.stage = 'DISCOVERY'; }
      break;
    }
    case 'DISCOVERY': {
      if (!next.userDraw && t.length > 3) next.userDraw = text.slice(0, 300);
      const p = detectPersona(t);
      // D-002: only advance if persona detected OR user explicitly signals
      if (p) { next.matchedPersona = p; next.stage = 'PERSONA_ALIGNMENT'; }
      else if (CUSTOMER_INTENT.test(t) || /\b(yes|ok|sure|1|2|3|4)\b/.test(t)) {
        // treat "1/2/3/4" as persona choice
        const num = t.match(/\b([1-4])\b/)?.[1];
        if (num === '1') next.matchedPersona = 'becky';
        else if (num === '2') next.matchedPersona = 'mistress_keysha';
        else if (num === '3') next.matchedPersona = 'switch_muse';
        else if (num === '4') next.matchedPersona = 'keysha_seductress';
        if (next.matchedPersona) next.stage = 'PERSONA_ALIGNMENT';
      }
      // else: stay in DISCOVERY, Maxine re-asks softly
      break;
    }
    case 'PERSONA_ALIGNMENT': if (t.length > 5) next.stage = 'GRAND_SLAM_OFFER'; break;
    case 'GRAND_SLAM_OFFER':
      if (PRICE_OBJ.test(t)) { next.objectionsEncountered.push(text.slice(0, 200)); next.stage = 'OBJECTION_HANDLING'; }
      else if (CLOSE_INTENT.test(t)) next.stage = 'CLOSING_SLOT';
      break;
    case 'OBJECTION_HANDLING': if (CLOSE_INTENT.test(t)) next.stage = 'CLOSING_SLOT'; break;
    case 'CLOSING_SLOT': if (CLOSE_INTENT.test(t) || /\b(yes|ok|sure|do it|book it)\b/i.test(t)) next.stage = 'CLOSED'; break;
  }
  return next;
}
