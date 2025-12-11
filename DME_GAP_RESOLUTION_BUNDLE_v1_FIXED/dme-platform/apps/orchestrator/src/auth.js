// Shared-secret based authentication middleware for orchestrator HTTP endpoints.

const config = {
  orchSharedSecret: process.env.ORCH_SHARED_SECRET
};

if (!config.orchSharedSecret) {
  // Hard fail at startup if secret is missing.
  throw new Error(
    'ORCH_SHARED_SECRET must be configured. Refusing to start unprotected orchestrator.'
  );
}

export function authMiddleware(req, res, next) {
  const sharedSecret = req.headers['x-dme-auth-secret'];
  if (sharedSecret !== config.orchSharedSecret) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  return next();
}
