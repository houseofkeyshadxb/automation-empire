# HOUSE OF KEYSHA EMPIRE — FULL BLUEPRINT & HISTORY
**Date:** October 2026
**Scope:** Complete architecture, legacy code, new code, and future roadmap.

---

## PART 1: THE MAXINE WHATSAPP BOT (CURRENT LIVE SYSTEM)
*The system currently running on Vercel and OpenClaw.*

### 1.1 Tech Stack
*   **Frontend/API:** Next.js 14 (App Router) on Vercel.
*   **Database:** Supabase.
*   **AI Router:** Groq API (`qwen/qwen3.8-27b`).
*   **Transport:** OpenClaw (linked to +971 54 778 3323).

### 1.2 Routing & Delivery Logic
*   **Delivery Drivers:** Detected via `lib/ai/delivery.ts`. Replies with building address (`Al Yousef Tower 2`).
*   **Spam/Wrong Number:** Detected via `lib/ai/intent-parser.ts`. Replies "I think you may have the wrong number" and closes.
*   **Customers:** Routed to the Funnel.

### 1.3 The Sales Funnel (`lib/ai/closer-engine.ts`)
1. `AGE_GATE` -> 2. `DISCOVERY` -> 3. `PERSONA_ALIGNMENT` -> 4. `GRAND_SLAM_OFFER` -> 5. `OBJECTION_HANDLING` -> 6. `CLOSING_SLOT`.
*   **State Management:** Stored in Supabase table `reply_sessions` (JSONB).
*   **Pricing:** Hardcoded in `closer-engine.ts` (e.g., Keysha Initiation AED 2,500).

### 1.4 OpenClaw Configuration
*   File: `~/.openclaw/openclaw.json`
*   Provider: `maxine` (API: `openai-completions`, BaseURL: `https://house-of-keysha.vercel.app/api`).
*   **WARNING:** NEVER run `openclaw doctor` — it clobbers the custom provider and reverts to Ollama.

---

## PART 2: THE LEGACY TELEGRAM BOT (PHASE 1 DOCUMENT)
*The original 35-page spec you pasted. This is the foundation for future backend expansion.*

### 2.1 Tech Stack
*   **Framework:** grammY (TypeScript).
*   **AI Fallback Chain:** Groq -> Gemini -> Mistral -> OpenRouter.
*   **Database:** Supabase (30 tables).

### 2.2 The 30-Table CRM Schema (Legacy vs Current)
The original design had a massive 30-table schema (customers, conversations, messages, bookings, payments, media, social_posts, leads, availability_slots, campaigns, ai_runs, etc.). 
*   **Current State:** We migrated 12 core tables to the Next.js app using the `crm_` prefix (`crm_customers`, `crm_bookings`, etc.) to avoid collisions.
*   **Action:** The remaining 18 tables (ai_runs, ai_failures, audit_log, notifications, etc.) should be added when the corresponding features are built.

### 2.3 Payment & Idempotency Logic (From Phase 1 Spec)
*   **Webhook Idempotency:** The `webhook_events` table must use a `UNIQUE(provider, provider_event_id)` constraint to prevent double-processing.
*   **Entitlements:** `vault_entitlements` table maps a client to a media file. Only granted after a verified payment.
*   **Idempotency Gate:** Every webhook passes through `lib/payments/idempotency.ts` before touching the database.

---

## PART 3: THE N8N AUTOMATION BACKEND (COMMAND CENTRE)
*The 22-workflow architecture designed for WhatsApp Puppeteer automation.*

### 3.1 Workflows Overview
1.  `INBOUND_WHATSAPP`: Scrapes WhatsApp Web via Puppeteer.
2.  `MESSAGE_CLASSIFIER`: Identifies intent.
3.  `CLIENT_MEMORY`: Retrieves history.
4.  `AI_RESPONSE_ENGINE`: Generates response with fallback chain.
5.  `FLOW_MATCHER`: Matches predefined flows.
6.  `BOOKING_ENGINE`: Handles bookings.
7.  `CALENDAR_ENGINE`: Checks availability.
8.  `PAYMENT_ENGINE`: Generates payment links.
9.  `PAYMENT_CONFIRMATION`: Handles Stripe webhooks.
10. `FOLLOWUP_ENGINE`: Sends reminders based on state.
11. `GHOSTED_LEADS`: Re-engages inactive leads.
12. `SESSION_REMINDERS`: Sends 24h/2h reminders.
13. `POST_SESSION`: Generates briefings.
14. `CLIENT_RETENTION`: Re-engages old clients.
15. `UPSELL_ENGINE`: Suggests add-ons.
16. `BRIEFING_GENERATOR`: Uses AI to write session notes.
17. `CRM_SYNC`: Syncs with external CRM.
18. `ADMIN_ALERTS`: Sends Telegram notifications.
19. `AI_FAILURE_HANDLER`: Retries failed AI calls.
20. `DAILY_ANALYTICS`: Aggregates KPIs and sends reports.
21. `DATA_BACKUP`: Weekly backup to storage.
22. `ERROR_MONITOR`: Scans logs and restarts services.

### 3.2 The Puppeteer Microservice
*   Runs on port 3001.
*   Exposes `/send` and `/scrape` endpoints.
*   Uses `puppeteer-extra-plugin-stealth` to avoid detection.
*   Maintains session via `userDataDir`.

---

## PART 4: THE DATABASE MIGRATION HISTORY

### 4.1 The Legacy Migration (`001_consolidated.sql`)
The original schema had tables named `media`, `messages`, `bookings`, `payments`, etc.
*   **Issue:** Running `CREATE TABLE IF NOT EXISTS messages` failed because a `messages` table already existed with different columns.
*   **Fix:** Renamed the new tables to `crm_media`, `crm_messages`, `crm_bookings`, etc.
*   **Payment Router:** The old `payments` table (used by the Stripe/CCBill idempotency logic) was left untouched.

### 4.2 The Supabase RLS Security Model
*   All tables have Row Level Security (RLS) enabled.
*   The `service_role` key (used by the backend) bypasses RLS.
*   No `anon` policies exist, meaning the public API cannot read or write to the database.

---

## PART 5: FUTURE ROADMAP & UNRESOLVED ISSUES

### 5.1 Immediate Backlog (Next.js App)
*   **Task 1:** Contact Routing (Henry/Mom). Read `crm_contacts` at the start of `reply-beast.ts`. If relationship is friend/family, bypass funnel.
*   **Task 2:** Payment Integration. Wire `crm_payments` to a high-risk processor (CCBill, SegPay) or crypto gateway. Do not use Stripe/PayPal (they ban adult content).
*   **Task 3:** Media Vault. Upload 1,612 files to Supabase Storage buckets (`media-raw`, etc.) and populate `crm_media`.

### 5.2 Known Bugs
*   **Groq Model Retirement:** `qwen/qwen3.8-27b` is current, but Groq frequently retires models. Always check `/v1/models`.
*   **Env Var Mapping:** `GROQ_API_KEY` must contain exactly ONE key (no commas).
*   **WSL Permissions:** `~/.cache` must be a real Linux directory, not a symlink to `/mnt/d/`.

### 5.3 The "Master Command" for Future Agents
If you are an AI reading this, your job is to:
1.  Review `MASTER_HANDOVER.md` for the current live state.
2.  Review this file (`FULL_EMPIRE_BLUEPRINT.md`) for historical context.
3.  Do not introduce new schemas until the existing `crm_*` tables are populated and used.
