import { NextResponse } from "next/server";

export async function POST(req: Request) {
  // Use process.env directly (safe + works in Vercel build)
  const env = {
    STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
    NOWPAYMENTS_IPN_SECRET: process.env.NOWPAYMENTS_IPN_SECRET,
    REVOLUT_WEBHOOK_SECRET: process.env.REVOLUT_WEBHOOK_SECRET,
    BTCPAY_API_KEY: process.env.BTCPAY_API_KEY,
  };

  const sigStripe = req.headers.get("stripe-signature");
  const sigNow = req.headers.get("x-nowpayments-sig");
  const sigRevolut = req.headers.get("x-revolut-signature");
  const sigBtcpay = req.headers.get("x-btcpay-sig");

  // --- WEBHOOK VERIFICATION TODO (as per client spec) ---
  // For production you'll implement:
  // verifyStripeWebhook(req, env.STRIPE_WEBHOOK_SECRET)
  // verifyNowPayments(req, env.NOWPAYMENTS_IPN_SECRET)
  // verifyRevolut(req, env.REVOLUT_WEBHOOK_SECRET)
  // verifyBtcpay(req, env.BTCPAY_API_KEY)
  //
  // Then update subscription status, audit logs, geofence checks, etc.

  return NextResponse.json({
    ok: true,
    message: "Webhook received",
    provider_headers: {
      stripe: Boolean(sigStripe),
      nowpayments: Boolean(sigNow),
      revolut: Boolean(sigRevolut),
      btcpay: Boolean(sigBtcpay),
    },
  });
}
