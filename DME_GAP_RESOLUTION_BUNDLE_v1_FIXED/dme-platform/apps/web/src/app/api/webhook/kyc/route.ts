import { NextRequest, NextResponse } from 'next/server';

const ONFIDO_WEBHOOK_SECRET = process.env.ONFIDO_WEBHOOK_SECRET || '';

function verifyOnfidoSignature(rawBody: string, signature: string | null): boolean {
  // For simplicity we just compare a shared secret header; swap for HMAC if configured.
  if (!ONFIDO_WEBHOOK_SECRET) {
    throw new Error('ONFIDO_WEBHOOK_SECRET not configured');
  }
  return signature === ONFIDO_WEBHOOK_SECRET;
}

// Placeholder for DB update; wire to real repository in your environment.
async function updateUserKycStatus(applicantId: string, status: string) {
  console.log(`Updating KYC status for applicant ${applicantId} -> ${status}`);
}

export async function POST(req: NextRequest) {
  try {
    const rawBody = await req.text();
    const signature = req.headers.get('x-onfido-signature');

    if (!verifyOnfidoSignature(rawBody, signature)) {
      return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
    }

    const payload = JSON.parse(rawBody);
    const applicantId = payload.applicant_id || payload.object?.id;
    const status = payload.status || payload.object?.status;

    if (!applicantId || !status) {
      return NextResponse.json({ error: 'Malformed payload' }, { status: 400 });
    }

    await updateUserKycStatus(applicantId, status);

    return NextResponse.json({ received: true });
  } catch (err: any) {
    console.error('KYC webhook error', err);
    return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
  }
}
