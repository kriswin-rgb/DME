import { isNowPaymentsIpAllowed } from '../src/lib/nowpayments';

test('isNowPaymentsIpAllowed passes when whitelist empty', () => {
  process.env.NOWPAYMENTS_IP_WHITELIST = '';
  expect(isNowPaymentsIpAllowed('1.2.3.4')).toBe(true);
});
