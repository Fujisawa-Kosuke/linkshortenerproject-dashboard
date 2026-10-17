# Authentication

All authentication in this app is handled by **Clerk**. No other auth method, library, or custom implementation (NextAuth, Passport, hand-rolled sessions, password handling, etc.) may be used.

## Rules

1. **Clerk only** — use `@clerk/nextjs` for sign-in, sign-up, sessions, and user data.
2. **`/dashboard` is protected** — it (and everything under `/dashboard/*`) requires a signed-in user.
3. **Signed-in users are redirected from `/` to `/dashboard`.**
4. **Sign-in and sign-up always open as modals** — never as full pages or custom forms.

## Setup

- `<ClerkProvider>` wraps the app in [`app/layout.tsx`](../app/layout.tsx), with `signInFallbackRedirectUrl` and `signUpFallbackRedirectUrl` set to `/dashboard`.
- [`proxy.ts`](../proxy.ts) (Next.js 16's replacement for `middleware.ts`) runs `clerkMiddleware()` so `auth()` works in server code.
- Required env vars: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY` (see [environment-variables.md](./environment-variables.md)).

## Route Protection

Protect routes on the server. Never rely on hiding UI.

```tsx
// app/dashboard/page.tsx — protected
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const { userId } = await auth();
  if (!userId) redirect("/");
  // ...
}
```

```tsx
// app/page.tsx — homepage redirects signed-in users
export default async function Home() {
  const { userId } = await auth();
  if (userId) redirect("/dashboard");
  // ...
}
```

Any new page under `/dashboard/*` must perform the same `auth()` check (or be covered by a shared layout that does). The public `/l/[shortcode]` redirect route must stay unauthenticated.

## Sign In / Sign Up Modals

Always use `mode="modal"`:

```tsx
import { SignInButton, SignUpButton } from "@clerk/nextjs";

<SignInButton mode="modal">
  <Button variant="ghost">Sign In</Button>
</SignInButton>
<SignUpButton mode="modal">
  <Button>Sign Up</Button>
</SignUpButton>
```

- Do **not** create `/sign-in` or `/sign-up` pages, or use Clerk's `<SignIn />` / `<SignUp />` as full-page components.
- Do **not** use `mode="redirect"` (the default) — always set `mode="modal"` explicitly.
- Use `<SignedIn>`, `<SignedOut>`, and `<UserButton />` for conditional UI (see the header in `app/layout.tsx`). Use shadcn `Button` as the trigger child.

## Getting the User

| Context                         | API                                                              |
| ------------------------------- | ---------------------------------------------------------------- |
| Server Components, Server Actions | `const { userId } = await auth()` from `@clerk/nextjs/server`  |
| Full user object (server)       | `await currentUser()` from `@clerk/nextjs/server`                |
| Client Components (UI only)     | `useUser()` / `useAuth()` from `@clerk/nextjs`                   |

## Data Ownership

- Use the Clerk `userId` as the owner key on user data (e.g. `links.userId`).
- Never store passwords or auth secrets.
- Every Server Action must call `auth()` first and return `{ error: "Unauthorized" }` when there is no `userId`. Every `/data` helper that reads or mutates user rows must filter by `userId`. See [`data/links.ts`](../data/links.ts) and the server action rules in [`.github/instructions/server-actions.instructions.md`](../.github/instructions/server-actions.instructions.md).
- Never trust client-side auth state for authorization — always verify on the server.

## Do Not

- Add other auth libraries or custom auth/session/token code.
- Build custom sign-in/sign-up forms.
- Use full-page sign-in/sign-up flows.
- Skip the server-side `auth()` check on protected pages or actions.

## Troubleshooting

- **Not redirected after sign-in** — check `signInFallbackRedirectUrl` / `signUpFallbackRedirectUrl` on `ClerkProvider` and Clerk Dashboard redirect settings.
- **Auth state not updating / `auth()` errors** — confirm `ClerkProvider` wraps the app and `proxy.ts` is running `clerkMiddleware()`.
- **Protected route reachable while signed out** — add the `auth()` check to the page/layout; UI-only hiding is not protection.
