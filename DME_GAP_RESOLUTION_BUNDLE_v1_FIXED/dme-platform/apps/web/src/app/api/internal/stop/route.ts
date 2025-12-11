import { NextResponse } from 'next/server';

const CORE_SERVICE_KILL_SWITCH_URL =
  process.env.DME_CORE_KILL_SWITCH_URL || 'http://dme-core-v5:8080/api/v1/kill-switch';
const ORCHESTRATOR_INTERNAL_URL =
  process.env.ORCHESTRATOR_INTERNAL_URL || 'http://orchestrator:8081/killswitch/disable-sds';
const EMERGENCY_STOP_CODE = process.env.EMERGENCY_STOP_CODE;

type StopRequest = {
  code: string;
  reason?: string;
};

export async function POST(request: Request) {
  const body = (await request.json()) as StopRequest;
  const { code, reason } = body;

  if (!EMERGENCY_STOP_CODE) {
    return NextResponse.json(
      { message: 'Kill switch misconfigured: EMERGENCY_STOP_CODE not set.' },
      { status: 500 }
    );
  }

  if (code !== EMERGENCY_STOP_CODE) {
    return NextResponse.json({ message: 'Invalid stop code.' }, { status: 401 });
  }

  try {
    // 1. Trigger kill switch in backend core service
    const coreResp = await fetch(CORE_SERVICE_KILL_SWITCH_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: reason || 'Emergency stop invoked from web app' })
    });
    if (!coreResp.ok) {
      const errorText = await coreResp.text();
      throw new Error(`Core kill switch failed: ${coreResp.status} - ${errorText}`);
    }

    // 2. Ask orchestrator to disable SDS fanout
    const orchResp = await fetch(ORCHESTRATOR_INTERNAL_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-dme-auth-secret': process.env.ORCH_SHARED_SECRET || '' },
      body: JSON.stringify({ reason: reason || 'Kill switch active' })
    });
    if (!orchResp.ok) {
      const errorText = await orchResp.text();
      throw new Error(`Orchestrator SDS disable failed: ${orchResp.status} - ${errorText}`);
    }

    // 3. Log + notify (stubbed hook for n8n / Slack / email)
    console.log('ALERT: Kill switch activated. Notify founders, CISO, and Ops via automation.');

    return NextResponse.json(
      { message: 'Emergency Stop initiated', status: 'KILL_SWITCH_ACTIVE' },
      { status: 200 }
    );
  } catch (err: any) {
    console.error('Error during emergency stop execution', err);
    return NextResponse.json(
      { message: 'Kill switch command failed', error: err?.message || 'unknown' },
      { status: 500 }
    );
  }
}
