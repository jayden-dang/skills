// Provider registry. New providers must implement ProviderAdapter and pass CSRF review.
// Trap: GitHub org SSO requires enterprise app install — not the same as personal OAuth.
export type ProviderAdapter = {
  id: string;
  startAuth(redirectUri: string): string;
  handleCallback(code: string): Promise<{ externalId: string; email: string }>;
};

export const providers: Record<string, ProviderAdapter> = {
  google: {
    id: 'google',
    startAuth: (r) => `https://accounts.google.com?redirect=${r}`,
    handleCallback: async () => ({ externalId: 'g-1', email: 'a@b.com' }),
  },
};
