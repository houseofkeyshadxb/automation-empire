// Delivery driver detection — separate from customer/spam routing.
// Building + flat are env-configured. Flat sending is env-gated.

const DELIVERY_SERVICES = /\b(noon|amazon|careem|talabat|deliveroo|instashop|carrefour|aramax|aramex|dhl|fedex|smsa|naqel)\b/i;

// Fixed: Using new RegExp() for multi-line logic instead of /.../i literals
const DRIVER_PHRASES = new RegExp(
  "\\b(" +
  "i\\s+have\\s+(a\\s+|your\\s+)?(delivery|parcel|package|order)" +
  "|your\\s+(delivery|parcel|package|order)\\s+is\\s+(here|at|down|below|outside)" +
  "|(delivery|parcel|package)\\s+(boy|guy|driver|man)\\s+(here|at|arrived|downstairs|below)" +
  "|arrived\\s+at\\s+(the\\s+)?building" +
  "|at\\s+(the\\s+)?(reception|lobby|gate|entrance|security)" +
  "|coming\\s+to\\s+deliver" +
  "|drop[\\s-]?off" +
  "|delivering\\s+(a\\s+|your\\s+)?parcel" +
  "|where\\s+(should|do)\\s+i\\s+(deliver|drop|bring)" +
  "|which\\s+(flat|apartment|floor|building)" +
  ")\\b", "i"
);

const CUSTOMER_ASKING = new RegExp(
  "\\b(" +
  "where(?:'s| is)\\s+my\\s+(delivery|order|parcel)" +
  "|did\\s+you\\s+send\\s+(my|the)" +
  "|when\\s+will\\s+(my|the)\\s+(delivery|order|parcel)\\s+arrive" +
  "|track(?:ing)?\\s+(my|the)\\s+(order|delivery)" +
  ")\\b", "i"
);

export function detectDeliveryIntent(text: string): 'driver' | 'customer_asking' | null {
  const t = text.trim();
  if (!t) return null;
  if (CUSTOMER_ASKING.test(t)) return 'customer_asking';
  if (DRIVER_PHRASES.test(t)) return 'driver';
  if (DELIVERY_SERVICES.test(t) && /\b(here|at|arrived|coming|below|outside|downstairs|reception|door|deliver|drop)\b/i.test(t)) return 'driver';
  return null;
}

export function buildDeliveryReply(): string {
  const building = (process.env.DELIVERY_BUILDING || '').trim();
  const flat = (process.env.DELIVERY_FLAT || '').trim();
  const sendFlat = (process.env.DELIVERY_SEND_FLAT || 'false').toLowerCase() === 'true';

  if (!building) {
    // Not configured — fail safe, don't leak anything
    return "Thanks for the message — I'll be down shortly. Please wait at reception.";
  }
  if (sendFlat && flat) {
    return `Yes — ${building}, Apartment ${flat}. Please call when you arrive. Thank you.`;
  }
  return `${building} — please call when you arrive and I'll give the flat number. Thank you.`;
}
