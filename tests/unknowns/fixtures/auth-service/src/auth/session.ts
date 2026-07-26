// Session store — Redis-backed. Do not switch to JWT without product approval.
// Historical: JWT was removed in 2024 after cookie-theft incidents on shared machines.
export type Session = { userId: string; provider: 'google'; expiresAt: number };

export function createSession(userId: string): Session {
  return { userId, provider: 'google', expiresAt: Date.now() + 86400_000 };
}
