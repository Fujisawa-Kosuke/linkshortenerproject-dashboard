# UI Components

**All UI in this app is built with [shadcn/ui](https://ui.shadcn.com). Do NOT create custom UI components — always use shadcn/ui components.**

## Rules

1. Before writing any UI element, check whether shadcn/ui provides it. If it does, install and use it.
2. Never hand-roll primitives (buttons, inputs, dialogs, cards, selects, tables, badges, tooltips, etc.) or duplicate shadcn/ui functionality.
3. Never use raw HTML elements (`<button>`, `<input>`, `<select>`, `<textarea>`, `<table>`, …) with custom styling in place of the shadcn/ui equivalent.
4. Don't introduce other component libraries (MUI, Chakra, Radix themes, etc.).

## Installing Components

Add components with the shadcn CLI — don't copy code by hand or write files in `components/ui/` yourself:

```bash
npx shadcn@latest add <component-name>
```

- Components land in `components/ui/` (config: [`components.json`](../components.json) — style `new-york`, lucide icons, `@/components/ui` alias).
- Currently installed: `button`, `card`, `dialog`, `input`, `label`.
- Common ones to add as needed: `textarea`, `select`, `checkbox`, `switch`, `badge`, `table`, `tabs`, `dropdown-menu`, `tooltip`, `alert`, `skeleton`, `sonner` (toasts), `separator`, `sheet`, `popover`.

## Usage

Import from `@/components/ui/*` and compose:

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
      <CardContent>
        <Input placeholder="Enter text" />
        <Button>Submit</Button>
      </CardContent>
    </Card>
  );
}
```

## Customization

- Use component `variant` / `size` props first.
- Layer on Tailwind utilities through `className`, merged with `cn()` from `@/lib/utils`.
- Project-wide visual changes belong in theme tokens (`app/globals.css`) or, if unavoidable, the component source in `components/ui/`.

## Composition Is Allowed, Custom Primitives Are Not

- **OK:** feature-level components that _compose_ shadcn/ui parts, e.g. `CreateLinkDialog` in `app/dashboard/` built from `Dialog`, `Input`, `Label`, and `Button`.
- **Not OK:** a `CustomButton`, `MyModal`, `FancyInput`, or any component re-implementing something shadcn/ui already ships.
- Clerk's own components (`SignInButton`, `SignUpButton`, `UserButton`, etc.) are used per [authentication.md](./authentication.md); give their triggers a shadcn/ui `Button` child.

## Icons

Use `lucide-react` (the project's configured icon library).

## Do / Don't

```tsx
// ❌ Don't
export function CustomButton({ children, onClick }) {
  return (
    <button className="px-4 py-2 bg-blue-500 rounded" onClick={onClick}>
      {children}
    </button>
  );
}

// ✅ Do
import { Button } from "@/components/ui/button";

<Button onClick={handleClick}>Click Me</Button>;
```
