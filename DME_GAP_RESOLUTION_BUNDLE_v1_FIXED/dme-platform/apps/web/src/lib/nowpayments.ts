import crypto from 'crypto';

const NOWPAYMENTS_API_KEY = process.env.NOWPAYMENTS_API_KEY || '';
const NOWPAYMENTS_IP_WHITELIST = (process.env.NOWPAYMENTS_IP_WHITELIST || '').split(',').filter(Boolean);

export function verifyNowPaymentsSignature(rawBody: string, signature: string | null | undefined): boolean {
  if (!NOWPAYMENTS_API_KEY) {
    throw new Error('NOWPAYMENTS_API_KEY not configured');
  }
  if (!signature) {
    return false;
  }
  const hmac = crypto.createHmac('sha512', NOWPAYMENTS_API_KEY);
  hmac.update(rawBody);
  const expected = hmac.digest('hex');
  return expected === signature;
}

export function isNowPaymentsIpAllowed(ip: string | null | undefined): boolean {
  if (!NOWPAYMENTS_IP_WHITELIST.length) return true;
  if (!ip) return false;
  return NOWPAYMENTS_IP_WHITELIST.includes(ip);
}
