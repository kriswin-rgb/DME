import { NextRequest } from 'next/server';
import { POST } from '../src/app/api/webhook/payment/route';

test('returns error for unsupported provider', async () => {
  const req = new Request('https://example.com/api/webhook/payment', {
    method: 'POST',
    body: JSON.stringify({}),
    headers: { 'Content-Type': 'application/json' }
  }) as unknown as NextRequest;

  const res = await POST(req);
  expect(res.status).toBe(400);
});
