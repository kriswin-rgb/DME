import Stripe from 'stripe';

const stripeSecretKey = process.env.STRIPE_SECRET_KEY || '';
const stripeWebhookSecret = process.env.STRIPE_WEBHOOK_SECRET || '';

if (!stripeSecretKey) {
  console.warn('STRIPE_SECRET_KEY is not set. Stripe client cannot make live calls.');
}

export const stripe = stripeSecretKey
  ? new Stripe(stripeSecretKey, { apiVersion: '2024-06-20' })
  : null;

export function constructStripeEvent(
  payload: string | Buffer,
  signature: string | string[] | null | undefined
) {
  if (!stripe) {
    throw new Error('Stripe client not initialised');
  }
  if (!stripeWebhookSecret) {
    throw new Error('STRIPE_WEBHOOK_SECRET is not configured');
  }
  if (!signature) {
    throw new Error('Missing Stripe signature header');
  }

  const sig = Array.isArray(signature) ? signature[0] : signature;
  return stripe.webhooks.constructEvent(payload, sig, stripeWebhookSecret);
}
