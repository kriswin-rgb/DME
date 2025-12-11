import test, { beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';

let originalSecret;

beforeEach(() => {
  originalSecret = process.env.ORCH_SHARED_SECRET;
  process.env.ORCH_SHARED_SECRET = 'test-secret';
});

afterEach(() => {
  if (originalSecret !== undefined) {
    process.env.ORCH_SHARED_SECRET = originalSecret;
  } else {
    delete process.env.ORCH_SHARED_SECRET;
  }
});

const { authMiddleware } = await import('../src/auth.js');

function mockReq(secret) {
  return { headers: { 'x-dme-auth-secret': secret } };
}

function mockRes() {
  const res = { statusCode: 200, body: null };
  res.status = (code) => { res.statusCode = code; return res; };
  res.json = (b) => { res.body = b; return res; };
  return res;
}

test('authMiddleware accepts valid secret', () => {
  const req = mockReq('test-secret');
  const res = mockRes();
  let called = false;
  authMiddleware(req, res, () => { called = true; });
  assert.strictEqual(called, true);
  assert.strictEqual(res.statusCode, 200);
});

test('authMiddleware rejects invalid secret', () => {
  const req = mockReq('wrong-secret');
  const res = mockRes();
  let called = false;
  authMiddleware(req, res, () => { called = true; });
  assert.strictEqual(called, false);
  assert.strictEqual(res.statusCode, 401);
  assert.deepStrictEqual(res.body, { error: 'Unauthorized' });
});
