import express from 'express';
import { authMiddleware } from './auth.js';

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'orchestrator' });
});

app.post('/killswitch/disable-sds', authMiddleware, (req, res) => {
  const { reason } = req.body || {};
  console.log('Disabling SDS fanout. Reason:', reason);
  // In production, this would update config / feature flags / redis.
  res.json({ status: 'sds_disabled', reason });
});

const port = process.env.PORT || 8081;
app.listen(port, () => {
  console.log(`DME Orchestrator listening on ${port}`);
});
