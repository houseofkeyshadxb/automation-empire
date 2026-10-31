# House of Keysha: Message Routing & Response Generation System
## Complete Execution Audit & Defect Register
**Conducted**: 2026-10-30

---

## EXECUTION PATH MAP

### 1. Incoming Message Flow (Entry Point)

```
Client (WhatsApp/Telegram/API) 
  ↓
POST /api/chat/completions 
  (route.ts: 21-28)
  ↓
Security check (MAXINE_SECRET) 
  ↓
Extract messages array from body
  ↓
stableSessionKey(body, messages)
  [Line 8-12: FIRST COLLISION RISK]
  ↓
generateMaxineReply({ sessionKey, messages })
```

**Entry File**: `app/api/chat/completions/route.ts` (25 lines)
**Entry Function**: `POST(req: NextRequest)`

---

### 2. Funnel State Retrieval & Processing

```
generateMaxineReply() 
  (reply-beast.ts: 24-44)
  ↓
getFunnelStateFromDB(sessionKey)
  (funnel-state.ts: 6-12)
  ↓
[DB: reply_sessions table]
  ├─ session_key (PK)
  ├─ funnel: { stage, ageVerified, userDraw, matchedPersona, objectionsEncountered, lastInteractionAt }
  └─ updated_at
  ↓
Extract last user message:
  lastUser = messages.find(m => role === 'user')
  userText = lastUser?.content || ''
  ↓
evaluateNextStage(current, userText)
  (intent-parser.ts: 31-61)
```

**Database File**: Supabase PostgreSQL (`reply_sessions` table)
**State Management**: `lib/ai/funnel-state.ts`
**Routing Logic**: `lib/ai/intent-parser.ts`

---

### 3. Stage Routing & Intent Detection

```
evaluateNextStage(cur: FunnelContext, text: string) → FunnelContext
│
├─ Step 1: Normalize
│   text = text.toLowerCase().trim()
│   Create next state: { ...cur, lastInteractionAt: Date.now() }
│
├─ Step 2: Global Pattern Checks (any stage)
│   ├─ HUMAN_INTENT: /\b(human|real person|manager|...)\b/i
│   │  → IMMEDIATELY route to HUMAN_HANDOFF
│   │
│   └─ NOT_CUSTOMER (line 36):
│       ├─ isNotCustomer(text) checks SPAM_PATTERNS (lines 3-12)
│       ├─ ONLY applied when stage === 'AGE_GATE' ⚠️ BUG: Spam patterns ignored after age verification
│       └─ If matched → stage = 'CLOSED'
│
├─ Step 3: Stage-Specific Logic
│   │
│   ├─ AGE_GATE (stage on line 38-44)
│   │  Input: Unverified new contact
│   │  Logic:
│   │    • under = /i'm (19|20)|under 21|too young|minor|below 21/i
│   │      → HUMAN_HANDOFF
│   │    • yes = /21\+|2[1-9]|[3-9]\d|adult|yes|confirm|agree|affirmative/i
│   │      → ageVerified = true → DISCOVERY
│   │    • [else]
│   │      → stay in AGE_GATE (no state change)
│   │
│   ├─ DISCOVERY (stage on line 45-51)
│   │  Input: Age verified; discovering user's draw & matching persona
│   │  Logic:
│   │    • Store first user message if > 3 chars: userDraw = text[0:300]
│   │    • Try detect persona from text
│   │      ├─ becky: /becky|1|one|submissive|in control|lead|boss|in charge/i
│   │      ├─ mistress_keysha: /keysha|mistress|2|two|let go|controlled|submit|surrender/i
│   │      ├─ switch_muse: /3|three|both|switch|dual/i
│   │      └─ keysha_seductress: /pepper|4|hotwife|mommy|goddess|seductress|tease/i
│   │    • If persona detected → matchedPersona = p, stage = PERSONA_ALIGNMENT
│   │    • Else if userDraw exists AND text > 20 chars
│   │      → AUTO-DEFAULT persona to mistress_keysha ⚠️ BUG: Assumes without asking
│   │      → stage = PERSONA_ALIGNMENT
│   │
│   ├─ PERSONA_ALIGNMENT (stage on line 52)
│   │  Input: Persona matched; deepening investment
│   │  Logic:
│   │    • If text > 5 chars → GRAND_SLAM_OFFER
│   │    • [else] → stay in PERSONA_ALIGNMENT
│   │
│   ├─ GRAND_SLAM_OFFER (stage on line 53-56)
│   │  Input: Ready to present offer; testing for objections
│   │  Logic:
│   │    • if PRICE_OBJ: /cheaper|discount|expensive|too much|afford|budget|reduce|costly|steep/i
│   │      → Add objection to list
│   │      → stage = OBJECTION_HANDLING
│   │    • else if CLOSE_INTENT: /book|reserve|slot|screening|deposit|confirm|tonight|tomorrow|when can|let's do it|i'm in/i
│   │      → stage = CLOSING_SLOT
│   │    • [else] → stay in GRAND_SLAM_OFFER
│   │
│   ├─ OBJECTION_HANDLING (stage on line 57)
│   │  Input: User hesitating on price/terms
│   │  Logic:
│   │    • if CLOSE_INTENT → stage = CLOSING_SLOT
│   │    • [else] → stay in OBJECTION_HANDLING
│   │
│   ├─ CLOSING_SLOT (stage on line 58)
│   │  Input: User ready to book
│   │  Logic:
│   │    • if CLOSE_INTENT OR /yes|ok|sure|do it|book it/i
│   │      → stage = CLOSED
│   │
│   ├─ HUMAN_HANDOFF (stage line 17-18)
│   │  [No internal routing logic]
│   │
│   └─ CLOSED (stage line 18)
│      [No internal routing logic]
│
└─ Return: next (updated FunnelContext)
```

**Routing File**: `lib/ai/intent-parser.ts` (62 lines)

---

### 4. System Prompt Building

```
buildCloserSystemPrompt(ctx: FunnelContext) → string
  (closer-engine.ts: 21-23)
  ↓
stageDirective(ctx)
  (closer-engine.ts: 8-20)
  ↓
Switch on ctx.stage:
  ├─ AGE_GATE
  │  "OBJECTIVE: Confirm 21+. Warm, luxurious. ONE yes/no question. 
  │   NO prices, NO services, NO House details."
  │
  ├─ DISCOVERY
  │  "OBJECTIVE: Discover driver + match persona. Acknowledge smoothly, 
  │   then ask TWO questions: (a) What drew you in today? 
  │   (b) Which dynamic fits you best: 1) control, 2) let go, 
  │   3) both/switch, 4) specific fantasy? NO pricing yet."
  │
  ├─ PERSONA_ALIGNMENT
  │  "OBJECTIVE: Deepen investment. Persona matched: ${persona.label}.
  │   Ask TWO diagnostic questions: How long have you wanted...?
  │   What happens if you keep suppressing...? NO pricing yet."
  │
  ├─ GRAND_SLAM_OFFER
  │  "OBJECTIVE: Present Grand Slam. Experience: ${persona.label}.
  │   Value stack: ${inclusions.join(' + ')} — anchor AED ${valueStack}.
  │   Their investment: AED ${initiationPrice}. Guarantee: respected, safe.
  │   Scarcity: 3 new clients/week. End: Should we reserve screening..."
  │
  ├─ OBJECTION_HANDLING
  │  "OBJECTIVE: Handle hesitation WITHOUT discounting. Ask what missing.
  │   Offer tier-down: 60-min Standard AED ${standardPrice} or 
  │   90-min Initiation AED ${initiationPrice}. Which gives you...?"
  │
  ├─ CLOSING_SLOT
  │  "OBJECTIVE: Secure the slot. Confirm time. State: Keysha's office 
  │   will reach out to finalize verification. Do NOT confirm yourself."
  │
  ├─ HUMAN_HANDOFF
  │  "OBJECTIVE: Handoff. Say a team member stepping in. Do not sell."
  │
  └─ CLOSED
     "OBJECTIVE: Post-close grace. Confirm politely. No re-pitch."
  ↓
Return system prompt:
  "YOU ARE MAXINE: elite sovereign curator for House of Keysha, Dubai. 
   High-status, discreet, luxurious. Never desperate, never robotic. 
   Never mention being AI. Never invent prices. Under 60 words. 
   One question max.
   
   ${stageDirective}"
```

**System Prompt File**: `lib/ai/closer-engine.ts` (24 lines)
**Persona Profiles**: Defined in closer-engine.ts lines 2-7

---

### 5. LLM Chain Execution & Response Sanitization

```
buildChain() 
  (reply-beast.ts: 5-12)
  ↓
Return array of LLM providers (in order):
  ├─ Groq (qwen/qwen3.8-27b)
  ├─ Gemini (gemini-2.0-flash)
  ├─ Mistral (mistral-small-latest)
  └─ OpenRouter (meta-llama/llama-3.3-70b-instruct:free)
  ↓
For each provider:
  ├─ POST to provider API with:
  │  ├─ model
  │  ├─ messages: [{ role: system, content: systemPrompt }, ...last 20 messages]
  │  ├─ max_tokens: 500
  │  ├─ temperature: 0.85
  │  └─ timeout: 15 seconds
  │
  └─ If response OK:
     └─ text = response.choices[0].message.content
        ↓
        sanitize(text)
          (reply-beast.ts: 18-22)
          ├─ allowedPrices(): Extract { 700, 1400, 2800, 1200, 2500, 5000, 1100, 2200, 4400, 1000, 1900, 3800 }
          ├─ Replace unapproved prices: /\b(\d{2,6})\s*AED\b/gi → "the listed price"
          ├─ Replace discount language: /\b(discount|cheaper|...)\b/gi → "a bonus"
          └─ Return sanitized text
        ↓
        saveFunnelState(sessionKey, next)
          (funnel-state.ts: 14-16)
          → UPSERT to reply_sessions table
        ↓
        Return { text, provider }

If all providers fail or no text:
  └─ FORCE: stage = HUMAN_HANDOFF
  └─ Return { text: "A moment — I'll have Keysha's office follow up personally.", provider: 'fallback' }
```

**LLM Orchestration File**: `lib/ai/reply-beast.ts` (45 lines)

---

### 6. API Response

```
NextResponse.json({
  id: `chatcmpl-${Date.now()}`,
  object: 'chat.completion',
  created: Math.floor(Date.now() / 1000),
  model: 'maxine',
  choices: [{
    index: 0,
    message: { role: 'assistant', content: text },
    finish_reason: 'stop'
  }],
  usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
  provider: provider_name
})
```

---

## CRITICAL DEFECT REGISTER

### 🔴 **P0: Blocking Defects**

| ID | File | Line | Issue | Impact | Evidence |
|---|---|---|---|---|---|
| **D-001** | `intent-parser.ts` | 11 | Bare greeting pattern `/^.{0,3}$/` closes funnel immediately | "hi" from friend gets CLOSED instead of waiting for next message | `isNotCustomer("hi")` returns true on first message; stage becomes CLOSED |
| **D-002** | `intent-parser.ts` | 49 | Auto-default persona to mistress_keysha without user selection | User gets wrong persona; no way to correct choice | If `text.length > 20` and no persona detected, auto-assigns mistress_keysha |
| **D-003** | `intent-parser.ts` | 36 | Spam patterns only checked in AGE_GATE, ignored after age verification | Spam/ham in DISCOVERY+ stages can trigger LLM calls and DB saves | `if (isNotCustomer(text) && cur.stage === 'AGE_GATE')` has explicit stage gate |
| **D-004** | `intent-parser.ts` | N/A | No CASUAL greeting pattern → can't distinguish "hi" from "hi bot test" | Both treated same; no smart routing to "Hey 💫" response | Current patterns: SPAM_PATTERNS, HUMAN_INTENT, PRICE_OBJ, CLOSE_INTENT; no CASUAL |
| **D-005** | `intent-parser.ts` | N/A | No CUSTOMER_INTENT pattern for booking signals | "I want to book a session" in AGE_GATE doesn't auto-trigger age check | No regex to detect: book, price, service, available, rate, session, hire, appointment |
| **D-006** | `intent-parser.ts` | 38-44 | AGE_GATE logic doesn't handle "I'm 25, what's this about?" → stays in AGE_GATE | User's valid age confirmation is treated as a "maybe later" response | Age regex `/\b(21\+?|2[1-9]|[3-9]\d|...)\b/` will catch "25" but needs explicit question asked first |
| **D-007** | `reply-beast.ts` | 39 | State saved BEFORE sanitization | If LLM injects bad price, DB has clean state but user sees dirty text | `sanitize()` happens after `saveFunnelState()` on line 39 |
| **D-008** | `route.ts` | 8 | Session key hash collision risk | Two users' identical first messages get same session ID & shared state | `let h = 0; for (...) h = (h * 31 + charCode) \| 0; return 'anon-${Math.abs(h)}'` |

---

### 🟡 **P1: High-Priority Defects**

| ID | File | Line | Issue | Impact | Evidence |
|---|---|---|---|---|---|
| **D-009** | `intent-parser.ts` | 39-40 | AGE_GATE yes/no regex too permissive | "I want the 25-minute session" (contains "25") triggers age verify pass | `/\b(21\+?|2[1-9]|[3-9]\d|...)\b/i` matches any 2-digit+ number, including prices/durations |
| **D-010** | `intent-parser.ts` | 25-28 | Persona detection regex overlaps & order-dependent | "in control" matches both becky AND mistress_keysha; Mistress Keysha tested second so wins | Ambiguous keywords: "in control" could mean "I'm in control" (becky) or "under control" (mistress_keysha) |
| **D-011** | `intent-parser.ts` | 21 | PRICE_OBJ pattern weak on affordability questions | "what if I can't afford this" doesn't match; "any cheaper" does | Missing: afford, minimum, payment plan, install, budget, minimum spend |
| **D-012** | `closer-engine.ts` | N/A | No feedback loop for persona correction | If Maxine guesses persona wrong (becky when user wants mistress_keysha), no way to re-route | System assumes persona is locked once PERSONA_ALIGNMENT stage reached |
| **D-013** | `reply-beast.ts` | 30-42 | If all LLM providers fail, forces HUMAN_HANDOFF without trying to respond gracefully | User sees "A moment — Keysha's office..." but doesn't know why | No exponential backoff, no retry count, no failure logging |
| **D-014** | `funnel-state.ts` | 7-12 | Empty funnel created & inserted on every request if session doesn't exist | DB bloat; performance issue; no cleanup | `getFunnelStateFromDB()` creates row even for spam sessions that get closed immediately |
| **D-015** | `intent-parser.ts` | 45-50 | userDraw captures first 300 chars AFTER age verification in DISCOVERY | userDraw misses the actual first message (the age-gate response) | `text.slice(0, 300)` captures response to "are you 21?", not user's opening draw |

---

### 🟠 **P2: Medium-Priority Defects**

| ID | File | Line | Issue | Impact | Evidence |
|---|---|---|---|---|---|
| **D-016** | `intent-parser.ts` | 22 | CLOSE_INTENT includes "confirm" but system never asks "confirm yes?" | Creates false positives where user says "I'll confirm later" (stays in CLOSING_SLOT) | Pattern: `/book\|reserve\|slot\|screening\|deposit\|confirm\|.../i` |
| **D-017** | `closer-engine.ts` | 14 | GRAND_SLAM_OFFER directive includes "Scarcity: 3 new clients/week" | If Maxine repeats this, it's no longer scarcity language (user hears same thing every message) | Pressure tactic diminishes with repetition |
| **D-018** | `intent-parser.ts` | 35 | HUMAN_INTENT check happens BEFORE stage gate check (line 36) | If user says "I need a real person" in GRAND_SLAM_OFFER, routed to HUMAN_HANDOFF correctly, but... | Order: HUMAN_INTENT (line 35) → NOT_CUSTOMER (line 36) means HUMAN_INTENT has priority (correct, but could be clearer) |
| **D-019** | `reply-beast.ts` | 13-16 | allowedPrices() rebuilds Set on every call | Minor performance issue; should be cached | Called inside sanitize() which is called on every response |
| **D-020** | `closer-engine.ts` | 2-7 | Persona prices hardcoded in closer-engine.ts | If prices change, code must be redeployed (not a DB config) | PERSONA_PROFILES is a static object, not fetched from DB |
| **D-021** | N/A | N/A | No test coverage for: greetings, mixed intent, bookings, price objections, persona selection, ambiguity, handoff | Unknown failure modes; untested edge cases | No test files found in repo |
| **D-022** | `intent-parser.ts` | 50 | Fallback persona logic: `else if (next.userDraw && t.length > 20)` assumes userDraw is set | If userDraw not yet set (edge case), persona stays undefined → PERSONA_ALIGNMENT without persona | `next.userDraw` could be undefined; no null check |

---

## ROUTING RULE CONFLICTS

### Conflict #1: Greeting Override
**Severity**: P0 (blocks happy path)

| Input | Current Behavior | Correct Behavior |
|---|---|---|
| "hi" (from friend, first message) | isNotCustomer("hi") = true → CLOSED | Should stay in AGE_GATE & get "Hey 💫" |
| "hi I want to book" (mixed intent, 18 chars) | Passes 1-3 char filter; no CUSTOMER_INTENT pattern → stays AGE_GATE; system asks "are you 21?" | Detects CUSTOMER_INTENT → asks age immediately |
| "hi" + later "what is this?" | First: CLOSED. Later: session already closed. | First: AGE_GATE. Later: gets "who's this?" routing. |

**Root Cause**: Line 11 pattern `/^.{0,3}$/` treats all short messages (incl. greetings) as spam.

---

### Conflict #2: Persona Auto-Assignment Precedence
**Severity**: P0 (wrong persona = wrong offer)

| Input | Current Behavior | Issue |
|---|---|---|
| "I like being in control" (after age gate) | Matches becky regex line 25 → persona = becky | But then line 26 checks mistress_keysha `/let go\|controlled\|submit\|surrender/` which might also match context → order matters |
| "I'm not sure, just exploring" (25+ chars, no keywords) | Line 49: AUTO-defaults to mistress_keysha | User never asked for Mistress; system assumed. No way to correct. |
| "what about the tease option?" (mentions "tease" → keysha_seductress) | Line 28 detects keysha_seductress → correct | But if earlier message already set matchedPersona in DISCOVERY, this line never runs (line 47-49 logic) |

**Root Cause**: No DISCOVERY clarification step; auto-default treats ambiguity as "Mistress Keysha" without user input.

---

### Conflict #3: Age Gate Logic Doesn't Match New Design
**Severity**: P0 (breaks bare greeting flow)

| Input | Current Logic | Your New Design |
|---|---|---|
| "hi" | isNotCustomer checks line 36; CLOSED | CASUAL pattern → stays AGE_GATE, reply "Hey 💫" |
| "hi I want to book" | No CUSTOMER_INTENT pattern; treated same as "hi" | CUSTOMER_INTENT pattern → ask age immediately |
| "I'm 22" in first message | no /21\|22/i in SPAM_PATTERNS; if age-related msg is first, passes through; then age gate asks; user answers age. Valid. | User says age in first msg → AGE_GATE handler detects it → moves to DISCOVERY |

**Root Cause**: Current system has no CASUAL or CUSTOMER_INTENT patterns; relies only on SPAM_PATTERNS.

---

## MISSING PATTERNS & REGEX GAPS

### Pattern: CASUAL (Missing)
**Current Code**: None
**Should Be**: `/^(hi|hey|hello|yo|sup|hiya|howdy|good (morning|afternoon|evening)|what'?s up|wsg)[.!?]*$/i`
**Handles**:
- "hi"
- "hey 😊"
- "hello?"
- "what's up" (39 chars, but matches pattern)
- "good morning" (12 chars, matches)

**Gap**: Currently no way to detect these → all short messages close funnel.

---

### Pattern: CUSTOMER_INTENT (Missing)
**Current Code**: None
**Should Be**: `/\b(book|booking|price|pricing|cost|rate|rates|service|services|available|availability|session|sessions|massage|companion|companionship|hire|appointment|slot|menu|offer|treatment)\b/i`
**Handles**:
- "how much for a booking?"
- "are you available tonight?"
- "what's your rate?"
- "I want to book Keysha"
- "do you offer companion services?"

**Gap**: Currently, these messages aren't distinguished from "I'm confused" → no fast-path to age gate.

---

### Pattern: NOT_CUSTOMER (Exists but incomplete)
**Current Code** (lines 3-12):
```typescript
const SPAM_PATTERNS = [
  /\b(wrong number|wrong person|sorry wrong)\b/i,
  /\b(delivery|parcel|courier|your order|food delivery|package)\b/i,
  /\b(job|hiring|resume|cv|application|interview)\b/i,
  /\b(seo|marketing agency|grow your (instagram|business)|promote your)\b/i,
  /\b(crypto|invest(ment)? opportunity|forex|trading signals)\b/i,
  /\b(loan|credit card|insurance offer)\b/i,
  /\b(hi{3,}|test(ing)?|asdf|random)\b/i,
  /^.{0,3}$/,  // ← PROBLEM: catches "hi", "hey", "how"
];
```

**New Design** (from your proposal):
```typescript
const NOT_CUSTOMER = /\b(wrong (number|person)|sorry wrong|delivery|parcel|courier|your order|food delivery|package|job|hiring|resume|cv|application|interview|seo|marketing agency|grow your|promote your|crypto|invest(ment)? opportunity|forex|trading signals|loan|credit card|insurance offer)\b/i;
```

**Gaps in NOT_CUSTOMER**:
- Doesn't catch `/^.{0,3}$/` (good — that's the bug)
- Doesn't catch `hi{3,}|test|asdf|random` (should they?)
- Misses: robocall patterns, obviously-automated patterns (e.g., "⚠️ ALERT:", "🚀 URGENT")

---

### Pattern: PRICE_OBJ (Exists but weak)
**Current Code** (line 21):
```typescript
/\b(cheaper|discount|expensive|too much|afford|budget|reduce|costly|steep)\b/i
```

**Gaps**:
- ✓ Catches: "that's too expensive", "is it cheaper?", "my budget is 500"
- ✗ Misses: "what if I can't afford", "is there payment plan", "minimum spend?", "any installment", "what's the lowest?"

---

### Pattern: CLOSE_INTENT (Exists but includes false positives)
**Current Code** (line 22):
```typescript
/\b(book|reserve|slot|screening|deposit|confirm|tonight|tomorrow|when can|let'?s do it|i'?m in)\b/i
```

**Gaps**:
- ✓ Catches: "let's book for tonight", "reserve a slot", "I'm in"
- ✗ False positives: "I need to confirm with my partner first", "when can you tell me more?" (contains "when can")
- ✗ Misses: "yes let's do this", "sign me up", "let's go", "make it happen"

---

### Persona Detection Ambiguities

| Regex | Keyword | Matches Personas | Issue |
|---|---|---|---|
| becky | "in control" | becky (line 25) | But could mean "I want to be in control" (wrong persona) |
| becky | "lead" | becky | Same: could mean user wants to lead (belongs to mistress_keysha) |
| mistress_keysha | "let go" | mistress_keysha | Unambiguous ✓ |
| mistress_keysha | "controlled" | mistress_keysha | Could mean "I want controlled experiences" (ambiguous) |
| keysha_seductress | "tease" | keysha_seductress | Unambiguous ✓ |
| keysha_seductress | "goddess" | keysha_seductress | Could be "I want to worship a goddess" (ambiguous) |

**Problem**: Order of regex checks matters. Line 25 (becky) checked before line 26 (mistress_keysha).
If message: "I want to be in control and make decisions", matches line 25 (becky regex) first → assigns becky, never checks mistress_keysha.

---

## EXECUTION TEST MATRIX

### Test Set 1: Greetings & Initial Routing

| Test ID | Input | Session State | Expected Stage | Expected Behavior | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|---|
| **T-001** | "hi" | New (AGE_GATE, unverified) | AGE_GATE | "Hey 💫" reply, wait for next | CLOSED ❌ | FAIL |
| **T-002** | "hey 😊" | New (AGE_GATE, unverified) | AGE_GATE | "Hey 💫" reply, wait | CLOSED ❌ | FAIL |
| **T-003** | "hello?" | New (AGE_GATE, unverified) | AGE_GATE | "Hey 💫" reply, wait | CLOSED ❌ | FAIL |
| **T-004** | "wrong number" | New (AGE_GATE, unverified) | CLOSED | "No worries 💫" | CLOSED ✓ | PASS |
| **T-005** | "hi" + session → "who is this" | AGE_GATE after greeting | AGE_GATE | "Hey — private line, who's this?" | Unknown (session closed at T-001) | FAIL |

---

### Test Set 2: Mixed Intent (Greeting + Business)

| Test ID | Input | Session State | Expected Stage | Expected Behavior | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|---|
| **T-006** | "hi I want to book" | New | AGE_GATE | Detects CUSTOMER_INTENT; asks "are you 21?" | No CUSTOMER_INTENT pattern; stays AGE_GATE without asking age ❌ | FAIL |
| **T-007** | "how much for a 90 min session" | New | AGE_GATE | CUSTOMER_INTENT detected; asks age | Stays AGE_GATE, might ask age (depends on "90" number matching age regex) ⚠️ | FAIL |
| **T-008** | "hello, what's the price?" | New | AGE_GATE | CUSTOMER_INTENT detected; asks age | Stays AGE_GATE without age question ❌ | FAIL |

---

### Test Set 3: Age Verification

| Test ID | Input (after "are you 21?") | Session State | Expected Stage | Expected Behavior | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|---|
| **T-009** | "yes" | AGE_GATE, unverified | DISCOVERY | Move to DISCOVERY; ask "what drew you in?" | DISCOVERY ✓ | PASS |
| **T-010** | "I'm 25" | AGE_GATE, unverified | DISCOVERY | Detects age "25"; moves to DISCOVERY | DISCOVERY ✓ (regex catches "25") | PASS |
| **T-011** | "I'm under 18" | AGE_GATE, unverified | HUMAN_HANDOFF | Route to human; don't pitch | HUMAN_HANDOFF ✓ | PASS |
| **T-012** | "what do you mean?" | AGE_GATE, unverified | AGE_GATE | Re-ask age or clarify | Stays AGE_GATE; no state change ⚠️ | FAIL |

---

### Test Set 4: Persona Selection

| Test ID | Input (in DISCOVERY) | Expected Persona | Expected Stage | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|---|
| **T-013** | "I want to let go completely" | mistress_keysha | PERSONA_ALIGNMENT | Detects mistress_keysha ✓ | PASS |
| **T-014** | "I like being in control" | becky | PERSONA_ALIGNMENT | Detects becky ✓ (but ambiguous) | PASS |
| **T-015** | "I'm not sure, just exploring" (35 chars) | mistress_keysha (default) | PERSONA_ALIGNMENT | AUTO-defaults to mistress_keysha ❌ | FAIL (auto-default without asking) |
| **T-016** | "tell me about the goddess option" | keysha_seductress | PERSONA_ALIGNMENT | Detects keysha_seductress from "goddess" ✓ | PASS |
| **T-017** | "I want to worship a goddess" | Should clarify; could be keysha_seductress OR becky worship fantasy | ? | Matches keysha_seductress regex; no clarification ❌ | FAIL |

---

### Test Set 5: Pricing & Objections

| Test ID | Input (in GRAND_SLAM_OFFER) | Expected Stage | Expected Behavior | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|---|
| **T-018** | "that's expensive" | OBJECTION_HANDLING | Detect price objection; move stage | OBJECTION_HANDLING ✓ | PASS |
| **T-019** | "what if I can't afford this" | OBJECTION_HANDLING | Detect affordability objection | Doesn't match PRICE_OBJ pattern ❌ | FAIL |
| **T-020** | "is there a payment plan?" | OBJECTION_HANDLING | Detect implicit price concern | Doesn't match pattern ❌ | FAIL |
| **T-021** | "let's do it" | CLOSING_SLOT | Detect closing intent; move stage | CLOSING_SLOT ✓ | PASS |
| **T-022** | "when can I book?" | CLOSING_SLOT | Detect booking intent | CLOSING_SLOT ✓ (matches "when can") | PASS |

---

### Test Set 6: Edge Cases & False Positives

| Test ID | Input | Session State | Expected | Current Behavior | Pass/Fail |
|---|---|---|---|---|---|
| **T-023** | "I want the 25-minute session" | GRAND_SLAM_OFFER | Discuss session options | If somehow in AGE_GATE, "25" regex matches age ✓; but shouldn't be in AGE_GATE | FAIL (if routed wrong) |
| **T-024** | Empty message "" | Any | No state change | No state change ✓ (line 34) | PASS |
| **T-025** | Message > 500 chars (pasted essay) | DISCOVERY | Store first 300 chars as userDraw; move on | Stores first 300 ✓ | PASS |
| **T-026** | "Hi, I need to talk to a real human" | Any | HUMAN_HANDOFF | HUMAN_HANDOFF ✓ (line 35) | PASS |
| **T-027** | Same first message from 2 different numbers | New (both) | Different session IDs | Hash collision possible with basic hash ❌ | FAIL (D-008) |

---

### Test Set 7: Human Handoff & Closure

| Test ID | Input | Expected Behavior | Current Behavior | Pass/Fail |
|---|---|---|---|---|
| **T-028** | All LLM providers fail (no API key, network down) | Route to HUMAN_HANDOFF; send fallback message | Routes to HUMAN_HANDOFF; returns "A moment — Keysha's office..." ✓ | PASS |
| **T-029** | Message after CLOSED stage | No state change; repeat polite closure | Stays CLOSED; Maxine repeats closure ✓ | PASS |
| **T-030** | Ambiguous message in CLOSING_SLOT | Clarify intent or confirm booking | Stays in CLOSING_SLOT; system repeats offer ⚠️ | FAIL (no clarification logic) |

---

## ROOT CAUSE ANALYSIS

### Root Cause #1: Over-Aggressive Spam Detection
**Symptom**: "hi" closes funnel instead of waiting
**Root Cause**: Line 11 pattern `/^.{0,3}$/` treats all 1-3 char messages as spam
**Why It Happened**: Spam filter was too broad; assumed short messages = bots; didn't account for genuine greetings
**Affected Defects**: D-001
**Correct Fix**: Remove `/^.{0,3}$/` from SPAM_PATTERNS; add CASUAL pattern; add CUSTOMER_INTENT pattern

---

### Root Cause #2: No Explicit Greeting Recognition
**Symptom**: "hey" and "hi" don't get special "Hey 💫" response
**Root Cause**: No CASUAL pattern in regex suite
**Why It Happened**: System assumed all intent could be routed with SPAM_PATTERNS + stage logic; missed greeting-as-signal
**Affected Defects**: D-004
**Correct Fix**: Add CASUAL pattern; update AGE_GATE stage directive to handle bare greetings

---

### Root Cause #3: Missing Business Intent Signal
**Symptom**: "I want to book" in first message doesn't trigger age verification
**Root Cause**: No CUSTOMER_INTENT pattern; system can't distinguish "hi" from "how much for a session?"
**Why It Happened**: System relied on multi-turn assumption (user says hi → system asks age → user responds). Didn't account for users who show intent upfront.
**Affected Defects**: D-005
**Correct Fix**: Add CUSTOMER_INTENT pattern; update AGE_GATE logic to ask age immediately if CUSTOMER_INTENT detected

---

### Root Cause #4: Persona Auto-Default Without User Input
**Symptom**: "I'm exploring" gets persona = mistress_keysha without user asking
**Root Cause**: Line 49 logic assumes if message > 20 chars and no persona keyword, default to mistress_keysha
**Why It Happened**: Presumed long message = user is engaged enough for a guess; tried to avoid bottleneck in DISCOVERY
**Affected Defects**: D-002, D-015
**Correct Fix**: Remove auto-default; keep in DISCOVERY until user explicitly selects persona; update Maxine prompt to ask "which dynamic fits you?"

---

### Root Cause #5: Age Gate Yes/No Regex Too Permissive
**Symptom**: "I want the 25-minute session" can trigger age verification pass
**Root Cause**: `/\b(21\+?|2[1-9]|[3-9]\d|...)\b/i` matches ANY 2+ digit number
**Why It Happened**: Regex prioritized recall (catch all ages) over precision; assumed if user says age, they're answering age gate question
**Affected Defects**: D-009
**Correct Fix**: Make age detection more explicit; only in response to age gate question; add context requirement

---

### Root Cause #6: Spam Pattern Scope Limited to AGE_GATE
**Symptom**: Spam/unrelated messages in DISCOVERY+ don't get closed
**Root Cause**: Line 36 check `if (isNotCustomer(text) && cur.stage === 'AGE_GATE')`
**Why It Happened**: Assumed once user passes age gate, they're legitimate; but spam can slip through with fake age response
**Affected Defects**: D-003
**Correct Fix**: Keep NOT_CUSTOMER check in ALL stages until CLOSING_SLOT; allow escape hatch for any-stage spam

---

### Root Cause #7: Session ID Hash Collision Risk
**Symptom**: Two users with same first message get same session ID
**Root Cause**: Line 8 uses basic polynomial hash without salt/seed
**Why It Happened**: Implemented fast anon session ID; didn't consider collision impact (shared funnel state = disaster)
**Affected Defects**: D-008
**Correct Fix**: Use crypto.randomUUID() for anon sessions; seed hash with timestamp or random value

---

## SMALLEST SAFE CORRECTION RECOMMENDATION

### Priority 1: Unblock the Happy Path (Fix D-001, D-004, D-005)

**Changes**:
1. **intent-parser.ts**: Replace `SPAM_PATTERNS` array with cleaner NOT_CUSTOMER regex (remove `/^.{0,3}$/`)
2. **intent-parser.ts**: Add CASUAL pattern for bare greetings
3. **intent-parser.ts**: Add CUSTOMER_INTENT pattern for booking signals
4. **intent-parser.ts**: Update AGE_GATE stage logic to:
   - NOT close on CASUAL message; stay in AGE_GATE and get "Hey 💫" from Maxine
   - Immediately ask age if CUSTOMER_INTENT detected
5. **closer-engine.ts**: Update AGE_GATE directive to handle bare greeting case

**Files Modified**: 2 (intent-parser.ts, closer-engine.ts)
**Lines Changed**: ~20 lines
**Risk**: Low (additive patterns; no logic inversions)

---

### Priority 2: Fix Persona Auto-Default (Fix D-002, D-015)

**Changes**:
1. **intent-parser.ts**: Remove lines 48-49 auto-default logic in DISCOVERY case
2. **closer-engine.ts**: Ensure DISCOVERY directive explicitly asks for persona selection

**Files Modified**: 2
**Lines Changed**: ~3 lines removed
**Risk**: Low (removes feature that wasn't working)

---

### Priority 3: Fix Age Regex Collision (Fix D-009)

**Changes**:
1. **intent-parser.ts**: Tighten age detection regex to exclude price/duration numbers
2. Add context requirement: only match if previous system message mentioned age

**Files Modified**: 1
**Lines Changed**: ~2 lines
**Risk**: Medium (behavior change; might miss some legitimate age responses)

---

### NOT Recommended in Initial Fix:

- D-003 (spam pattern scope): Requires careful testing across all stages; defer
- D-008 (hash collision): Requires session architecture decision; defer
- D-007 (state save before sanitize): Requires transaction semantics; defer
- D-010 (persona regex overlap): Needs clearer keyword taxonomy; defer
- D-020 (hardcoded prices): Requires DB migration; defer

---

## TEST COVERAGE GAPS

| Test Coverage | Current | Needed | Priority |
|---|---|---|---|
| Unit tests for intent-parser.ts | 0 | ✓ All patterns | P0 |
| Integration tests for message flow | 0 | ✓ Full funnel | P0 |
| Edge case tests (greetings, mixed intent) | 0 | ✓ T-001 to T-030 | P1 |
| Persona selection disambiguation | 0 | ✓ T-013 to T-017 | P1 |
| Price objection detection | 0 | ✓ T-018 to T-022 | P1 |
| LLM provider fallback | 0 | ✓ T-028 | P2 |
| Session isolation (hash collision) | 0 | ✓ D-008 scenario | P2 |

---

## FILES & DEPENDENCIES SUMMARY

| File | Purpose | Dependencies | Risk Level |
|---|---|---|---|
| `lib/ai/intent-parser.ts` | Stage routing & pattern detection | None (pure functions) | HIGH (core logic) |
| `lib/ai/closer-engine.ts` | System prompt building + persona profiles | funnel-state.ts (type) | MEDIUM (content-heavy) |
| `lib/ai/reply-beast.ts` | LLM orchestration | funnel-state.ts, intent-parser.ts, closer-engine.ts | HIGH (orchestration) |
| `lib/ai/funnel-state.ts` | DB I/O + state types | supabase/server.ts | MEDIUM (DB schema risk) |
| `app/api/chat/completions/route.ts` | API entry point | reply-beast.ts | LOW (thin wrapper) |
| `supabase/migrations/` | DB schema | (empty; schema presumed in Supabase) | HIGH (unknown state) |

---

## CONCLUSION

**Status**: System has **8 blocking defects** preventing correct greeting & booking flow.

**Root Cause**: Over-aggressive spam filtering (pattern `/^.{0,3}$/`) + missing CASUAL & CUSTOMER_INTENT patterns.

**Smallest Safe Fix**: Implement signal-strength-based routing (your proposed design):
1. Add CASUAL pattern for bare greetings → "Hey 💫" + wait
2. Add CUSTOMER_INTENT pattern for booking signals → ask age immediately
3. Remove hardcoded 1-3 char spam pattern
4. Update AGE_GATE stage directive accordingly

**Implementation Cost**: ~20 lines across 2 files; low risk.

**Testing**: Need matrix covering all 30 test cases before deploying.

