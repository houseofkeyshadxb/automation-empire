import { createClient, type SupabaseClient } from '@supabase/supabase-js';
let _db: SupabaseClient | null = null;
export function getDb(): SupabaseClient {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) throw new Error('Supabase env missing: SUPABASE_URL and SUPABASE_SERVICE_KEY required');
  if (!_db) _db = createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
  return _db;
}
