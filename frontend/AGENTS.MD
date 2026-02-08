## Project Stack

- Next.js (App Router)
- React + TypeScript
- React Query (@tanstack/react-query)
- Zod (runtime validation)
- Storybook (UI development)
- TailwindCSS (styling)

---

## High-Level Architecture

**Data & control flow:**

UI Components → Feature Hooks → Feature Services → Backend API

Layer Role Knows About

---

Components Rendering & interaction Props, hooks
Hooks Server state + UI logic Services, React Query
Services API communication Endpoints, schemas
Schemas Runtime validation API payload shapes
Types Static typing Derived from schemas when possible

---

## Golden Rule

> Prefer simple, explicit, and testable code over clever abstractions.

If something feels "smart", it is probably wrong for this codebase.

---

## LLM Operational Rules

### 1. Never Invent Contracts

The agent **must not hallucinate**:

- API endpoints\
- Request/response fields\
- Query parameters\
- Environment variables\
- Feature flags

If the contract is unclear:

- Reuse an existing pattern
- Search for similar services/hooks
- Add a `TODO: confirm backend contract`
- Do **not** fabricate fields

---

### 2. Respect Layer Boundaries

---

If you are editing... You MAY You MUST NOT

---

Component Render UI, Fetch data, call APIs
call hooks

Hook Use React Write JSX, call fetch
Query, call directly
ONE service

Service Call API, map Use React, store UI
data state

Schema Validate Contain UI logic
runtime data

---

---

### 3. Components (UI Layer)

**Purpose:** Rendering only.

**Rules:**

- Keep components small and composable
- Receive data via props or hooks
- Show loading, error, and empty states
- Extract reusable UI pieces instead of duplicating markup

**Never:**

- Call APIs
- Contain business rules
- Transform raw API payloads

---

### 4. Hooks (Feature Logic Layer)

**Purpose:** Orchestrate server state and UI behavior.

**Rules:**

- One main responsibility per hook
- Use React Query for all server data
- Call exactly **one** service function per query/mutation
- Return clean values: `{ data, isLoading, error, actions }`

**Never:**

- Render UI
- Contain large data transformations
- Call `fetch` directly

---

### 5. Services (API Layer)

**Purpose:** Isolate all API communication.

**Rules:**

- One file per feature service group
- Use centralized API client from `src/api`
- Perform **light** response mapping only
- Validate important responses with Zod when safety matters

**Never:**

- Use React
- Use browser APIs
- Store state
- Contain JSX

---

### 6. Zod Schemas

Zod defines **runtime truth**.

Use schemas for:

- API response parsing
- Form validation
- Shared data contracts

Guidelines:

- Prefer `z.infer<typeof Schema>` for types
- Do not duplicate types that already exist as schemas
- Keep schemas close to the feature

---

### 7. Server vs Client Components

**Server Components**

- Fetch initial/static data only
- No React client hooks
- No browser APIs

**Client Components**

- Interactive UI
- Event handlers
- React Query usage

Never move interactive logic into Server Components.

---

### 8. Data Fetching Standards

Data Type Tool

---

Server data React Query
Local UI state useState / useReducer
Forms React Hook Form + Zod (if present)

Do not use `useEffect` for data fetching.

---

### 9. Error Handling

- Services throw structured errors
- Hooks expose error states
- Components render user-friendly messages
- Never silently ignore API failures
- **Always use the backend's error message** — when the API returns an HTTPException, display its `detail` text instead of hardcoding frontend messages
- **Minimalist error UI** — show errors as plain red text (`text-(--color-error)`), no background boxes, no extra padding or border-radius wrappers

---

### 10. Accessibility

All generated UI must:

- Use semantic HTML
- Include labels for inputs
- Be keyboard accessible
- Avoid clickable `<div>` patterns

---

### 11. Performance Awareness

Avoid:

- Duplicate queries
- Unnecessary re-renders
- Large client bundles from server-only logic

Prefer:

- React Query caching
- Colocation by feature
- Lazy loading heavy UI blocks

---

### 12. Storybook Rules

**Every new component MUST have a corresponding Storybook story.**

- Create a `.stories.tsx` file **next to** the component (same directory)
- Cover **every possible state**: default, loading, error, disabled, empty, hover, active variants
- Use **mock data** — never real API calls
- Mock data lives in the story file itself or in a shared `__mocks__/` folder if reused across stories
- Name stories with the `PascalCase` component name (e.g., `Button.stories.tsx`)
- Use `satisfies Meta<typeof Component>` for type safety
- Add `args` and `argTypes` for interactive controls where meaningful
- For components that depend on providers (QueryClient, Toast), use the global decorators from `.storybook/preview.ts`

**Story structure example:**
```tsx
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { MyComponent } from "./my-component";

const meta = {
  title: "shared/MyComponent",  // or "features/main/MyComponent"
  component: MyComponent,
} satisfies Meta<typeof MyComponent>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { ... } };
export const Loading: Story = { args: { ... } };
export const Error: Story = { args: { ... } };
```

---

### 13. Code Style

- Clear, descriptive names
- No generic names like `data`, `stuff`, `helpers`
- Small focused files
- Prefer early returns over deep nesting

---

## Smells the Agent Must Avoid

- Fetch calls inside components
- Business logic inside JSX
- Massive "god components"
- Service functions used directly in UI
- Duplicated API logic
- State syncing hacks between components

---

## When Unsure

The agent should:

1.  Look for an existing similar feature
2.  Follow the same structure
3.  Leave a clear `TODO:` comment instead of guessing

---

This document defines **how the LLM must think before writing code** ---
not just how code should look.
