import * as stripeModule from '../src/lib/stripe';

test('constructStripeEvent throws when stripe not initialised', () => {
  const original = (stripeModule as any).stripe;
  (stripeModule as any).stripe = null;
  expect(() => stripeModule.constructStripeEvent('payload', 'sig')).toThrow(/not initialised/);
  (stripeModule as any).stripe = original;
});
