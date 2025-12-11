import { NextRequest } from 'next/server';
import { middleware } from '../src/middleware';

function createRequest(country?: string) {
  const url = 'https://example.com/';
  const req = {
    nextUrl: new URL(url),
    geo: country ? { country } : {},
    headers: new Headers()
  } as unknown as NextRequest;
  return req;
}

test('middleware blocks blocked country', () => {
  process.env.BLOCKED_COUNTRIES = 'GB,DE';
  const res = middleware(createRequest('GB'));
  expect(res?.headers.get('location')).toContain('/blocked');
});

test('middleware allows non-blocked country', () => {
  process.env.BLOCKED_COUNTRIES = 'GB,DE';
  const res = middleware(createRequest('US'));
  expect(res.headers.get('X-DME-App')).toBe('FinTech-Signals');
});
