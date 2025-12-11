import { NextRequest } from 'next/server';
import { POST } from '../src/app/api/internal/stop/route';

test('internal stop rejects invalid code', async () => {
  (process as any).env.EMERGENCY_STOP_CODE = 'secret-code';

  const body = JSON.stringify({ code: 'wrong' });
  const req = new Request('https://example.com/api/internal/stop', {
    method: 'POST',
    body,
    headers: { 'Content-Type': 'application/json' }
  }) as unknown as NextRequest;

  const res = await POST(req);
  const json = await res.json();
  expect(res.status).toBe(401);
  expect(json.message).toMatch(/Invalid/);
});
