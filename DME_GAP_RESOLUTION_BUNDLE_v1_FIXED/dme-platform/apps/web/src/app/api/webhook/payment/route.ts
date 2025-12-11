import { NextRequest, NextResponse } from 'next/server';

// --- STUBS for missing imports ---
function constructStripeEvent(rawBody: string, signature: string | null) {
  // Replace this stub with real Stripe verification logic
  return { type: 'stub_event', rawBody, signature };
}

function verifyNowPaymentsSignature(rawBody: string, signature: string | null) {
  // Replace this stub with real NOWPayments signature verification
  return true;
}

function isNowPaymentsIpAllowed(ip: string) {
  // Replace with actual allowed IPs logic
  return true;
}

// --- RATE LIMIT ---
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX_EVENTS = 100;
const recentEvents = new Map<string, { ts: number; count: number }>();

function assertWebhookRateLimit(key: string) {
  const now = Date.now();
  const entry = recentEvents.get(key);
  if (!entry || now - entry.ts > RATE_LIMIT_WINDOW_MS) {
    recentEvents.set(key, { ts: now, count: 1 });
    return;
  }
  entry.count += 1;
  if (entry.count > RATE_LIMIT_MAX_EVENTS) {
    throw new Error('Rate limit exceeded for webhook key ' + key);
  }
}

// --- WEBHOOK HANDLER ---
export async function POST(req: NextRequest) {
  const provider = req.nextUrl.searchParams.get('provider') || 'stripe';

  try {
    if (provider === 'stripe') {
      const rawBody = await req.text();
      const signature = req.headers.get('stripe-signature');
      assertWebhookRateLimit('stripe');
      const event = constructStripeEvent(rawBody, signature);

      console.log('Received Stripe webhook event:', event.type);
      return NextResponse.json({ received: true });
    }

    if (provider === 'nowpayments') {
      const rawBody = await req.text();
      const signature = req.headers.get('x-nowpayments-sig');
      const ip = req.ip ?? req.headers.get('x-forwarded-for') ?? '';

      if (!isNowPaymentsIpAllowed(typeof ip === 'string' ? ip.split(',')[0] : '')) {
        return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
      }

      assertWebhookRateLimit('nowpayments');

      const ok = verifyNowPaymentsSignature(rawBody, signature);
      if (!ok) {
        return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
      }

      const payload = JSON.parse(rawBody);
      console.log('Received NOWPayments webhook payload', payload.status);

      return NextResponse.json({ received: true });
    }

    return NextResponse.json({ error: 'Unknown provider' }, { status: 400 });
  } catch (err: any) {
    console.error('Payment webhook error', err);
    return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
  }
}
