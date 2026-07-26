# Auth module notes
- Sessions are Redis cookies only (see session.ts comment history).
- Adding a provider is an adapter plug-in, not a new table per provider.
- There is no `OAuthProvider` SQL table; linking is `user_identities(user_id, provider, external_id)`.
- Rate limit: 10 auth starts / IP / minute (edge middleware, not in this folder).
