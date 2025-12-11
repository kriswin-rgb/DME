import { authMiddleware } from '../auth.js';

function runMiddleware(mw, headers = {}) {
  const req = { headers };
  let statusCode = 200;
  const res = {
    status(code) { statusCode = code; return this; },
    json(body) { return { statusCode, body }; }
  };
  let calledNext = false;
  const next = () => { calledNext = true; };
  const result = mw(req, res, next);
  return { statusCode, calledNext, result };
}

// Note: this file is a simple smoke test stub for authMiddleware.
