import { NextRequest, NextResponse } from 'next/server';

const BLOCKED_COUNTRIES = (process.env.BLOCKED_COUNTRIES || 'GB,DE,FR,IT,ES').split(',');

export function middleware(req: NextRequest) {
  const country = req.geo?.country || '';

  if (BLOCKED_COUNTRIES.includes(country)) {
    const url = req.nextUrl.clone();
    url.pathname = '/blocked';
    return NextResponse.redirect(url);
  }

  const res = NextResponse.next();
  res.headers.set('X-DME-App', 'FinTech-Signals');
  res.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none';"
  );
  return res;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)']
};
