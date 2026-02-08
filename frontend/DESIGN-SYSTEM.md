# Design System — Carli

**Version:** 1.0
**Last Updated:** 2026-02-07

> This design system is based on the visual language established in the reference mockups.
> See the `images/` folder for the visual references used to derive these specifications.

### Conventions
- **TailwindCSS v4 shorthand syntax:** Use `property-(--token)` instead of `property-[var(--token)]`. Example: `py-(--space-4)` not `py-[var(--space-4)]`.
- **Animation library:** `motion` (v12+) for JS-driven animations. Import as `import * as m from "motion/react-client"`.
- **No top-level header:** The sidebar contains branding, navigation, and logout. Mobile uses a minimal hamburger bar.

---

## 1. Design Principles

1. **Mobile-first** — Design for the smallest screen first, then progressively enhance for larger viewports. Base styles target mobile; `min-width` media queries add complexity upward. Every component must work on a 320px viewport before any desktop enhancement is considered.
2. **Clarity over cleverness** — Every element should communicate its purpose immediately. DevOps tools are complex; the UI should not be.
3. **Density done right** — Show the information that matters without overwhelming. Use progressive disclosure — especially on small screens where space is scarce.
4. **Status at a glance** — Color, icons, and layout should make system health instantly readable on any device.
5. **Consistency** — Reuse the same components and patterns everywhere. Same problem, same solution.

---

## 2. Visual References

The following reference images establish the visual direction for Carli. They are from a related admin panel and should be adapted to Carli's CI/CD domain.

### 2.1 Projects List — Card View
![Projects List - Card View](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.57%20PM.jpeg)

**Key patterns to adopt:**
- Page title as large bold heading top-left
- Primary action button ("+ Crear Proyecto") top-right, dark rounded button
- Filter chips row below the title with colored status dots
- Search bar spanning most of the width with filter dropdowns on the right
- Summary KPI cards in a horizontal row (4 columns)
- Project cards in a responsive grid with category badge, status badge, title, metadata, and a budget/progress section
- Grid/Table view toggle (top-right of results area)

### 2.2 Sidebar Navigation — Expanded
![Sidebar Expanded](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.57%20PM%20(1).jpeg)

**Key patterns to adopt:**
- Sidebar shows user avatar + name + role at the top
- Navigation items with icons: Dashboard, Nuevo Proyecto, Reportes, Configuración
- Sidebar is white background, collapsible to icon-only mode
- Help widget at the bottom ("Necesitas Ayuda? Soporte: interno 2024")

### 2.3 Projects List — Table View
![Projects List - Table View](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.58%20PM%20(1).jpeg)

**Key patterns to adopt:**
- Same filters/search as card view at the top
- Table with columns: category badge, project name, location, status badge, budget, disbursed, progress bar, action icons
- Action icons per row: view (eye), edit (pen), approve (check), reject (X) — all circular icon buttons
- Pagination at bottom-right with rows-per-page selector

### 2.4 Project Detail — Header + Summary Cards
![Project Detail](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.58%20PM%20(2).jpeg)

**Key patterns to adopt:**
- Dark navy-to-blue gradient hero banner at the top of the detail page
- "Back" arrow link on the hero
- Category badge + status badge overlaid on the hero
- Project title (large, bold, white text on dark hero)
- Metadata line (location pin icon + address) below the title
- Action buttons top-right: "Aprobar", "Rechazar" (semantic ghost), "Editar" (secondary), "Exportar" (primary dark)
- Three summary cards below the hero in a 3-column grid:
  - Each card has an icon + title header
  - Content with key-value pairs and progress indicators

### 2.5 Confirmation Modal
![Confirmation Modal](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.59%20PM.jpeg)

**Key patterns to adopt:**
- Large green checkmark icon centered at the top of the modal
- Title: bold heading
- Subtitle: "Acción irreversible" warning in small gray text
- Read-only field showing project name
- Bullet list explaining consequences ("Lo que sucederá:")
- Two actions: "Cancelar" (ghost text) and "Confirmar" (primary green button with arrow)

### 2.6 Form Modal with Warning
![Form Modal](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.59%20PM%20(2).jpeg)

**Key patterns to adopt:**
- Large icon centered at top (dollar icon in rounded green square)
- Title + description text centered
- Form input with label, green focus border
- Helper text below the input (referencing a previous value)
- Yellow warning callout box with triangle icon and explanation text
- Actions: "Cancelar" (ghost) + "Confirmar" (dark primary button with checkmark)

### 2.7 Project Detail — Approved State with Toast
![Project Detail Approved](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.25.59%20PM%20(3).jpeg)

**Key patterns to adopt:**
- Same detail layout, but status badge changed to "Aprobado" (green)
- Summary cards now show additional data (Real vs Previsto budget)
- Description section as a full-width card below summary cards
- Success toast notification: bottom-center, green background, white text, icon + title + subtitle

### 2.8 Project Stages Section
![Project Stages](images/WhatsApp%20Unknown%202026-02-07%20at%206.26.06%20PM/WhatsApp%20Image%202026-02-07%20at%206.26.01%20PM%20(2).jpeg)

**Key patterns to adopt:**
- Section heading with icon ("Etapas del Proyecto")
- Grid/Table view toggle
- Stage cards showing: stage number badge, title, status badge, budget breakdown, progress bar, date range (estimated vs real), expandable description
- Action buttons per stage: "Desembolsos" (ghost), "Finalizar" (ghost), "Iniciar" (ghost with play icon)
- Footer with copyright, social links, and version indicator

---

## 3. Color Palette

### 3.1 Brand Colors

Derived from the reference images — a navy/dark-blue primary with teal-green accents.

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-brand-primary` | `#1B2559` | Top bar, hero banner gradient start, sidebar active states |
| `--color-brand-primary-light` | `#2D3A80` | Hero gradient end, hover states |
| `--color-brand-accent` | `#10B981` | Primary action buttons, success CTA, links |
| `--color-brand-accent-hover` | `#059669` | Hover state for accent |
| `--color-brand-accent-light` | `#ECFDF5` | Accent tinted backgrounds |
| `--color-brand-dark` | `#111827` | Primary CTA buttons ("+ Create Project", "Export") |
| `--color-brand-dark-hover` | `#1F2937` | Hover state for dark CTA |

### 3.2 Neutral Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-neutral-950` | `#0A0A0A` | Headings, primary text |
| `--color-neutral-700` | `#404040` | Body text |
| `--color-neutral-500` | `#737373` | Secondary text, placeholders, labels (uppercase) |
| `--color-neutral-300` | `#D4D4D4` | Borders, dividers |
| `--color-neutral-200` | `#E5E5E5` | Input borders, card borders |
| `--color-neutral-100` | `#F5F5F5` | Subtle backgrounds, hover rows, table headers |
| `--color-neutral-50` | `#FAFAFA` | Page background |
| `--color-white` | `#FFFFFF` | Cards, inputs, modals, sidebar |

### 3.3 Semantic Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-success` | `#22C55E` | Passed, Online, OK, Aprobado |
| `--color-success-light` | `#F0FDF4` | Success badge background |
| `--color-warning` | `#F59E0B` | Warnings, Pendiente status |
| `--color-warning-light` | `#FFFBEB` | Warning badge/callout background |
| `--color-error` | `#EF4444` | Errors, Failed, Rechazado, Offline |
| `--color-error-light` | `#FEF2F2` | Error badge background |
| `--color-info` | `#3B82F6` | En Ejecución, informational |
| `--color-info-light` | `#EFF6FF` | Info badge background |

### 3.4 Quality Gate Mapping

| Status | Background | Text | Border |
|--------|------------|------|--------|
| `OK` / Passed | `--color-success-light` | `#15803D` | `--color-success` |
| `WARN` / Warning | `--color-warning-light` | `#92400E` | `--color-warning` |
| `ERROR` / Failed | `--color-error-light` | `#B91C1C` | `--color-error` |

### 3.5 Stage / Environment Colors

| Stage | Color | Icon suggestion |
|-------|-------|----------------|
| Development | `#8B5CF6` (violet) | Code brackets `</>` |
| Staging | `#F59E0B` (amber) | Flask / beaker |
| Production | `#10B981` (emerald) | Globe |

---

## 4. Typography

**Font Family:** `Inter` (primary), `system-ui, -apple-system, sans-serif` (fallback)
**Monospace:** `JetBrains Mono`, `ui-monospace, monospace` (for URLs, code, tokens)

### 4.1 Type Scale

Font sizes below are the **mobile base**. On desktop (`min-width: 1024px`), `--text-display` scales up to `36px` and `--text-heading` to `24px`.

| Token | Size (mobile) | Size (desktop) | Weight | Line Height | Usage |
|-------|---------------|----------------|--------|-------------|-------|
| `--text-display` | `24px` | `30px` | `700` | `1.2` | Page titles ("Projects") — see ref 2.1 |
| `--text-heading` | `18px` | `20px` | `600` | `1.3` | Section headings ("Quality Gate", "Team Members") |
| `--text-subheading` | `15px` | `16px` | `600` | `1.4` | Card titles, form section labels |
| `--text-body` | `14px` | `14px` | `400` | `1.5` | Default body text |
| `--text-body-medium` | `14px` | `14px` | `500` | `1.5` | Emphasized body (table headers, labels) |
| `--text-label` | `11px` | `11px` | `700` | `1.3` | Uppercase labels ("TOTAL PROJECTS") — letter-spacing `0.05em` |
| `--text-small` | `12px` | `12px` | `400` | `1.5` | Captions, helper text, timestamps |
| `--text-mono` | `13px` | `13px` | `400` | `1.5` | URLs, code snippets (JetBrains Mono) |

### 4.2 Special Text Treatments

**Uppercase Labels** (seen in reference images for KPI cards, form labels, category badges):
- Font: `--text-label`
- Transform: `uppercase`
- Letter-spacing: `0.05em`
- Color: `--color-neutral-500`

**Hero Title** (project detail page):
- Mobile: `24px`, `font-weight: 700`, `--color-white`
- Desktop (`min-width: 1024px`): `36px`, `font-weight: 800`

---

## 5. Spacing

Use a **4px base unit**. All spacing is a multiple of 4.

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | `4px` | Tight inner gaps (icon-to-text, dot-to-label) |
| `--space-2` | `8px` | Compact padding, inline gaps, badge internal padding |
| `--space-3` | `12px` | Default inner padding |
| `--space-4` | `16px` | Standard gap between elements |
| `--space-5` | `20px` | Card inner padding |
| `--space-6` | `24px` | Section padding |
| `--space-8` | `32px` | Between cards / sections |
| `--space-10` | `40px` | Page-level top/bottom padding |
| `--space-12` | `48px` | Major section dividers |

---

## 6. Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | `6px` | Badges, tags, small chips, category pills |
| `--radius-md` | `8px` | Inputs, buttons |
| `--radius-lg` | `12px` | Cards, modals, panels, project cards |
| `--radius-xl` | `16px` | Large containers, hero cards, summary cards |
| `--radius-full` | `9999px` | Avatars, status dots, filter pills, action icon buttons |

---

## 7. Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift (inputs on focus) |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05)` | Project cards, summary cards |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05)` | Modals, dropdown panels |
| `--shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.05)` | Elevated modals, toast notifications |

---

## 8. Components

### 8.1 Buttons

> See reference images 2.4 (action buttons), 2.5 (modal actions), 2.6 (modal confirm).
>
> **Mobile-first note:** All buttons must have a minimum touch target of `44px` height on mobile. On desktop, buttons can be slightly smaller (`36px`) for compact layouts. Use `min-height` rather than fixed `height` so content can grow.

#### Primary Dark Button
As seen in "Crear Proyecto" and "Exportar" buttons.
- Background: `--color-brand-dark` (`#111827`)
- Text: `--color-white`
- Border radius: `--radius-full` (pill shape)
- Padding: `10px 24px`
- Font: `--text-body-medium`
- Icon: Left-aligned (e.g., `+` or download icon), `--space-2` gap
- Hover: `--color-brand-dark-hover`
- Disabled: `opacity: 0.5`, `cursor: not-allowed`
- Loading: Replace text with spinner, maintain button width

#### Primary Accent Button
As seen in "Confirmar Aprobación" button.
- Background: `--color-brand-accent` (`#10B981`)
- Text: `--color-white`
- Border radius: `--radius-md`
- Padding: `10px 24px`
- Icon: Right-aligned arrow or checkmark
- Hover: `--color-brand-accent-hover`

#### Secondary Button
As seen in "Editar" button.
- Background: `--color-white`
- Text: `--color-neutral-700`
- Border: `1px solid --color-neutral-300`
- Border radius: `--radius-full` (pill shape)
- Padding: `10px 20px`
- Icon: Left-aligned (pen icon)
- Hover: Background `--color-neutral-100`

#### Semantic Ghost Button
As seen in "Aprobar" (green) and "Rechazar" (red).
- Background: `transparent`
- Border: `1px solid` in semantic color
- Text + Icon: Semantic color
- Border radius: `--radius-full`
- Variants:
  - Success: `--color-success` border/text, checkmark icon
  - Danger: `--color-error` border/text, X icon

#### Ghost Text Button
As seen in "Cancelar" in modals.
- Background: `transparent`
- Text: `--color-neutral-500`
- No border
- Hover: Text `--color-neutral-700`

#### Circular Icon Button
As seen in table action buttons (view, edit, approve, reject).
- Size: `36px` circle
- Border radius: `--radius-full`
- Background: Semantic color (light variant) or `transparent`
- Icon: `18px`, semantic color
- Hover: Opacity `0.8`
- Variants: view (info), edit (warning), approve (success), reject (error)

### 8.2 Inputs

> See reference image 2.6 (form modal input) and 2.1 (search bar).

#### Text Input
- Height: `44px`
- Border: `1px solid --color-neutral-200`
- Border radius: `--radius-md`
- Padding: `0 16px`
- Font: `--text-body`
- Placeholder color: `--color-neutral-500`
- Focus: Border `--color-brand-accent`, shadow `0 0 0 3px rgba(16, 185, 129, 0.15)`
- Error: Border `--color-error`, helper text below in `--color-error`
- Disabled: Background `--color-neutral-100`, `cursor: not-allowed`

#### Search Input
As seen in the projects list filter bar.
- Same as Text Input with a `Search` icon (16px, `--color-neutral-500`) at the left
- Left padding: `44px` (to accommodate the icon)
- Full width within its container
- Placeholder: "Search by name..."

#### Textarea
- Same as Text Input but with `min-height: 100px`, `padding: 12px 16px`
- Resizable vertically

#### Select / Dropdown
As seen in the filter dropdowns ("Todas", "Todas las fechas").
- Same styling as Text Input
- Left icon (optional, e.g., calendar or grid icon), `--space-2` gap
- Chevron icon on the right side
- Dropdown panel: `--shadow-lg`, `--radius-lg`, max-height `240px` with scroll
- Selected option: `--color-brand-accent` text or checkmark

#### Form Label
- Font: `--text-label` (uppercase, 11px, weight 700)
- Color: `--color-neutral-500`
- Margin bottom: `--space-2`
- Letter-spacing: `0.05em`

#### Helper Text
- Font: `--text-small`
- Color: `--color-neutral-500`
- Error variant: `--color-error`

### 8.3 Cards

> See reference images 2.1 (project cards), 2.4 (summary cards), 2.8 (stage cards).

#### Project Card (List View)
As seen in reference 2.1.
- Background: `--color-white`
- Border: `1px solid --color-neutral-200`
- Border radius: `--radius-lg`
- Padding: `--space-5` (20px)
- Shadow: `--shadow-md`
- **Header row:** Category badge (left) + Status badge (right)
- **Body:** Project name (`--text-subheading`, bold), metadata line (icon + text, `--text-small`)
- **Footer section:** Separated by `1px solid --color-neutral-100` divider, showing key-value pairs (label uppercase, value bold), with optional progress bar
- Hover: `--shadow-lg`, subtle lift transform

#### Summary Card (Detail View)
As seen in reference 2.4 — three cards below the hero.
- Background: `--color-white`
- Border: `1px solid --color-neutral-200`
- Border radius: `--radius-xl`
- Padding: `--space-6`
- Shadow: `--shadow-md`
- **Header:** Colored icon circle (40px) + section title (`--text-subheading`)
- **Body:** Key-value pairs with uppercase labels and prominent values
- **Optional:** Thin progress bar, percentage text

#### Stage Card
As seen in reference 2.8.
- Same as Summary Card styling
- **Header:** Stage number badge (small, outlined) + Stage name + Status badge (right)
- **Body:** Budget breakdown, progress bar, date ranges (estimated vs real)
- **Footer:** Action buttons row (ghost style)

### 8.4 Hero Banner (Project Detail)

> See reference image 2.4.

- Background: Linear gradient from `--color-brand-primary` to `#2563EB` (left to right)
- Border radius: `0` (full-bleed on mobile) or `0 0 --radius-xl --radius-xl` on desktop
- **Content:**
  - Back link: `ArrowLeft` icon + "Back" text, `--color-white`, top-left
  - Category badge: dark background, white text, small pill
  - Status badge: colored pill
  - Metadata: icon + text, `--color-white` with `opacity: 0.8`

**Mobile (base):**
- Height: `auto` (min `140px`), padding: `--space-4`
- Title: `24px`, `font-weight: 700`
- Action buttons: **Not on hero** — rendered below it as a full-width button row
- Repository URL: Truncated with ellipsis, copy button

**Desktop (`min-width: 1024px`):**
- Height: `~200px`, padding: `--space-6`
- Title: `36px`, `font-weight: 800`
- Action buttons: Positioned absolute, top-right on the hero
- Repository URL: Fully visible

### 8.5 Badges / Status Indicators

> See reference images — status badges appear on every card and in tables.

#### Status Badge (Pill)
As seen throughout the reference images.
- Padding: `4px 12px`
- Border radius: `--radius-full`
- Font: `--text-small`, weight `600`
- Colored dot (6px circle) before text, `--space-1` gap
- Variants:

| Variant | Dot Color | Background | Text |
|---------|-----------|------------|------|
| Pending | `--color-warning` | `--color-white` | `--color-warning` |
| In Progress | `--color-info` | `--color-white` | `--color-info` |
| Approved / OK | `--color-success` | `--color-white` | `--color-success` |
| Rejected / Failed | `--color-error` | `--color-white` | `--color-error` |
| Completed | `--color-success` | `--color-success-light` | `#15803D` |

#### Category Badge
As seen in project cards (e.g., "OBRAS PUBLICAS", "SALUD").
- Padding: `4px 10px`
- Border radius: `--radius-sm`
- Background: `--color-neutral-100`
- Text: `--text-label` uppercase, `--color-neutral-700`
- Border: `1px solid --color-neutral-200`

**For Carli, use as Project Type badge:**
- "BACKEND" → `--color-neutral-100` background, `--color-neutral-700` text
- "FRONTEND" → `--color-neutral-100` background, `--color-neutral-700` text

#### Status Dot (Inline)
- Size: `8px` circle
- Colors: Same semantic colors as badges
- Used inline before text (e.g., "● Online")

### 8.6 KPI Summary Row

> See reference image 2.1 — four metric cards in a horizontal row.

- Container: Full-width, `display: grid`, `grid-template-columns: repeat(4, 1fr)`, `gap: --space-4`
- Each KPI card:
  - Background: `--color-white`
  - Border: `1px solid --color-neutral-200`
  - Border radius: `--radius-lg`
  - Padding: `--space-4`
  - **Icon:** 36px circle with semantic color background, white icon
  - **Label:** `--text-label` uppercase, `--color-neutral-500`
  - **Value:** `--text-heading`, `--color-neutral-950`, `font-weight: 700`

**For Carli, adapt to:**
- Total Projects (count)
- Quality OK (count of projects passing quality gate)
- Deployed (count of projects with production stage online)
- Alerts (count of recent incidents) — future feature

### 8.7 Filter Chips

> See reference image 2.1 — row of filter pills.

- Container: Horizontal flex row, `gap: --space-2`
- Each chip:
  - Padding: `6px 16px`
  - Border radius: `--radius-full`
  - Font: `--text-body-medium`
  - **Default (inactive):** Background `--color-white`, border `1px solid --color-neutral-200`, text `--color-neutral-700`
  - **Active:** Background `--color-brand-dark`, text `--color-white`, no border
  - Colored dot (6px) before text for status chips
  - Hover: Background `--color-neutral-100` (when inactive)

### 8.8 Toast / Notification

> See reference image 2.7 — success toast at bottom-center.

- Position: **Bottom-center**
- Border radius: `--radius-lg`
- Shadow: `--shadow-xl`
- Padding: `--space-4 --space-5`
- **Success variant:** Background `--color-brand-accent`, text `--color-white`
  - Icon (checkmark in circle) + Title (bold) + Subtitle (regular)
- **Error variant:** Background `--color-error`, text `--color-white`
- **Warning variant:** Background `--color-warning`, text `--color-white`
- Auto-dismiss after 5 seconds
- Enter: Fade-in + slide up from bottom
- Exit: Fade-out + slide down

**Mobile (base):**
- Width: `calc(100% - 2 * var(--space-4))` — full width with side margins
- Bottom offset: `--space-4` (above bottom nav if present)

**Desktop (`min-width: 768px`):**
- Width: `400px` max, centered

### 8.9 Warning Callout

> See reference image 2.6 — yellow warning box inside modal.

- Background: `--color-warning-light` (`#FFFBEB`)
- Border: none (or `1px solid #FDE68A` subtle)
- Border radius: `--radius-md`
- Padding: `--space-4`
- Icon: `AlertTriangle`, `--color-warning`, `20px`
- Text: `--text-small`, `--color-neutral-700`
- "Atención:" prefix in `font-weight: 600`

### 8.10 Modal / Dialog

> See reference images 2.5 and 2.6.

- Overlay: `rgba(0, 0, 0, 0.4)`
- **Top icon area:**
  - Large icon (48-56px) centered at top
  - Icon inside a colored rounded square or circle
  - Examples: Checkmark (green), Dollar sign (green), Warning (yellow)
- **Title:** `--text-heading`, centered, `--color-neutral-950`
- **Subtitle:** `--text-small`, centered, `--color-neutral-500`
- **Body:** Form fields or informational content
- **Actions:** Flex row, `justify-content: space-between` or centered
  - Left: Ghost text button ("Cancelar")
  - Right: Primary button (accent or dark)

**Mobile (base):**
- Container: Full-screen or near-full (`inset: --space-2` or `100vh` bottom sheet)
- Border radius: `--radius-xl --radius-xl 0 0` (bottom sheet) or `--radius-xl` (centered)
- Padding: `--space-6`
- Actions: Stacked vertically, full-width buttons, primary on top

**Desktop (`min-width: 768px`):**
- Container: Centered, `max-width: 480px`, `--radius-xl`, `--shadow-xl`
- Padding: `--space-8` top, `--space-6` sides and bottom
- Actions: Side-by-side row

### 8.11 Table

> See reference image 2.3.

- Container: Inside a Card (no extra border)
- **Header row:**
  - Background: `--color-neutral-50`
  - Text: `--text-label` uppercase, `--color-neutral-500`
  - Padding: `14px 16px`
- **Body rows:**
  - Text: `--text-body`, `--color-neutral-700`
  - Padding: `14px 16px`
  - Hover: Background `--color-neutral-50`
  - Border: Bottom `1px solid --color-neutral-100`
- **Action column:** Row of circular icon buttons (view, edit, approve, reject)
- **Pagination:**
  - Bottom-right alignment
  - "Showing 1-10 of N results" text (left)
  - Rows per page selector + page number buttons (right)
  - Active page: `--color-brand-accent` background circle, white text

**Mobile (base):**
- Table view is **hidden on mobile** — only card-list view is shown
- If table is rendered (e.g., in a detail section), wrap in a `overflow-x: auto` container for horizontal scroll
- Minimum column width: `120px`

**Desktop (`min-width: 768px`):**
- Table view becomes available via the Grid/Table toggle
- Full column layout visible

### 8.12 Progress Bar

> See reference images 2.1 (in cards), 2.8 (in stage cards).

- Height: `6px`
- Background (track): `--color-neutral-100`
- Border radius: `--radius-full`
- Fill: `--color-brand-accent` (or `--color-info` for in-progress)
- Percentage label: `--text-small`, `--color-brand-accent`, right-aligned

### 8.13 View Toggle (Grid / Table)

> See reference images 2.1 and 2.3 — top-right of results section.

- Two icon buttons side-by-side
- Grid icon: 2x2 grid squares
- Table icon: horizontal lines (list)
- Active: `--color-brand-dark` icon
- Inactive: `--color-neutral-300` icon
- Container: No background, `gap: --space-1`

### 8.14 Skeleton Loader

- Background: `--color-neutral-100`
- Border radius matches the element it replaces
- Shimmer animation: Left-to-right gradient sweep, `1.5s`, infinite
- Use on: cards, text lines, badges, KPI values

### 8.15 Empty State

- Centered in the content area
- Illustration or icon (64px, `--color-neutral-300`)
- Heading: `--text-heading`, `--color-neutral-700`
- Description: `--text-body`, `--color-neutral-500`
- CTA button (Primary Dark)

### 8.16 Avatar

- Sizes: `32px` (sidebar, small), `40px` (header), `48px` (profile)
- Border radius: `--radius-full`
- Fallback: Two-letter initials on `--color-brand-primary` background, `--color-white` text
- Border: `2px solid --color-white` (when on dark background)

### 8.17 Copy-to-Clipboard Button

- Icon button next to the text to copy
- Icon: `Copy` (16px), `--color-neutral-500`
- On click: Icon changes to `Check` in `--color-brand-accent` for 2 seconds
- Tooltip: "Copy" → "Copied!"

---

## 9. Layout (Mobile-First)

All layouts are defined **mobile-first**: the base state is a single-column, full-width layout with no sidebar. Complexity is added progressively via `min-width` breakpoints.

### 9.1 Application Shell

> **No top header.** The sidebar contains all navigation, branding, and the logout action. On mobile, a minimal top bar with hamburger + logo is shown.

#### Mobile Base (`< 768px`)

```
┌──────────────────────────┐
│  ☰  C  CARLI             │  ← Mobile top bar (56px, hamburger + logo)
├──────────────────────────┤
│                          │
│      CONTENT AREA        │  ← Full-width, padded
│      (single column)     │
│                          │
│                          │
│                          │
└──────────────────────────┘
```

- **No persistent header** — only a thin mobile bar with hamburger + Carli logo
- **Sidebar (drawer):** Slides in from left, `280px` wide, overlay behind
  - Logo "C" + "Carli" at top
  - Avatar + Name + Role below branding
  - Nav items (icon + label)
  - **Logout button at the bottom** (separated by border-top)
  - Close on overlay tap or X button
- **Content:** Full width, `padding: --space-4`

#### Tablet (`min-width: 768px`)

```
┌────┬─────────────────────────┐
│ C  │                         │
│ 👤 │                         │
│ ■  │     CONTENT AREA        │
│ ⊕  │     (2-column capable)  │
│    │                         │
│    │                         │
│ ⊕  │                         │
└────┴─────────────────────────┘
```

- **Collapsed sidebar:** `64px` wide, icon-only
- **Logout icon** at sidebar bottom
- **Content:** Fills remaining width, `padding: --space-6`

#### Desktop (`min-width: 1024px`)

```
┌──────────┬───────────────────────────────────────┐
│  C Carli │                                       │
│  ──────  │                                       │
│  Avatar  │                                       │
│  Name    │         CONTENT AREA                  │
│  Role    │         (multi-column)                │
│          │                                       │
│  ■ Proj  │                                       │
│  ⊕ New   │                                       │
│          │                                       │
│  ──────  │                                       │
│  ⊕ Logout│                                       │
└──────────┴───────────────────────────────────────┘
```

- **Expanded sidebar:** `240px`, `--color-white`, border-right
  - Logo "C" + "Carli" branding at top
  - Avatar (32px) + Name (bold) + Role (small, uppercase) below
  - Nav items: Icon (20px) + Label, `--space-3` vertical padding
    - Active: `--color-brand-primary` text
    - Hover: `--color-neutral-100` background
  - **Logout at bottom** — red hover state, separated by border-top
- **Content:** Max-width `1440px` (centered), `padding: --space-8` top, `--space-6` horizontal

### 9.2 Login Page

The login page is the same across all breakpoints — centered card, no shell.

- **Mobile (base):**
  - Full-screen, `--color-neutral-50` background
  - Card: Full width with `margin: --space-4`, `--radius-xl`, `--shadow-lg`
  - Logo + App name centered above form
  - Padding: `--space-6`
- **Tablet+ (`min-width: 768px`):**
  - Card: `max-width: 420px`, centered horizontally and vertically
  - Padding: `--space-8`

### 9.3 Projects List Page

> See reference images 2.1, 2.2, 2.3.

#### Mobile (base)

```
┌──────────────────────────┐
│  Projects            [+] │  ← Title + FAB or small button
│                          │
│  [All] [Pending] [OK] ►  │  ← Horizontal scroll chips
│                          │
│  ┌──────────────────────┐│
│  │ 🔍 Search...         ││  ← Full-width search
│  └──────────────────────┘│
│                          │
│  ┌──────┐ ┌──────┐      │  ← KPI: 2x2 grid
│  │Tot: 4│ │OK: 3 │      │
│  └──────┘ └──────┘      │
│  ┌──────┐ ┌──────┐      │
│  │Dep: 2│ │Alt: 1│      │
│  └──────┘ └──────┘      │
│                          │
│  4 results               │  ← No view toggle on mobile
│                          │
│  ┌──────────────────────┐│
│  │ Project Card 1       ││  ← Full-width stacked cards
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ Project Card 2       ││
│  └──────────────────────┘│
└──────────────────────────┘
```

- Title + "+" button on same row
- Filter chips: Horizontal scroll (`overflow-x: auto`, hide scrollbar), no wrap
- Search: Full width
- Filter dropdowns: Below search, stacked or in a collapsible "Filters" section
- KPI cards: `grid-template-columns: repeat(2, 1fr)`
- Project cards: `grid-template-columns: 1fr` (single column)
- **No table view** on mobile — card view only
- View toggle hidden

#### Tablet (`min-width: 768px`)

- KPI: `repeat(2, 1fr)` or `repeat(4, 1fr)` if space allows
- Project cards: `repeat(2, 1fr)`
- Search + filter dropdowns: Same row (flex-wrap)
- View toggle appears — grid/table switch available

#### Desktop (`min-width: 1280px`)

```
┌─────────────────────────────────────────────────────┐
│  Projects                           [+ New Project] │
│                                                     │
│  FILTER BY STATUS                                   │
│  [All] [Pending] [In Progress] [Passed] [Failed]    │
│                                                     │
│  ┌──────────────────────┐  [Filter ▼] [Date ▼]     │
│  │ 🔍 Search...          │                          │
│  └──────────────────────┘                           │
│                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │Total: 12 │ │ OK: 8    │ │Deploy: 6 │ │Alert: 2│ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│                                                     │
│  RESULTS: 12 projects              [Grid] [Table]   │
│                                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐               │
│  │Card 1│ │Card 2│ │Card 3│ │Card 4│               │
│  └──────┘ └──────┘ └──────┘ └──────┘               │
└─────────────────────────────────────────────────────┘
```

- KPI: `repeat(4, 1fr)`
- Cards: `repeat(auto-fill, minmax(300px, 1fr))`
- Full button text: "+ New Project"
- All filters visible in one row

### 9.4 Project Detail Page

> See reference images 2.4, 2.7, 2.8.

#### Mobile (base)

```
┌──────────────────────────┐
│  ← Back                  │
│  ┌──────────────────────┐│
│  │ [BACKEND] ● Passed   ││  ← Hero (shorter, ~140px)
│  │ Project Name         ││  ← Smaller font (24px)
│  │ 📍 git@...           ││
│  └──────────────────────┘│
│                          │
│  [Edit] [Export]         │  ← Action buttons below hero
│                          │
│  ┌──────────────────────┐│
│  │ Quality Gate         ││  ← Full-width stacked cards
│  │ ✓ Passed             ││
│  │ Coverage: 85%        ││
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ Deployments          ││
│  │ ● Dev: Online        ││
│  │ ○ Prod: Offline      ││
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ Team Members         ││
│  │ @john — Maintainer   ││
│  │ @jane — Developer    ││
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ Description          ││
│  │ Text...              ││
│  └──────────────────────┘│
└──────────────────────────┘
```

- Hero: Reduced height (`140px`), title at `24px`
- Action buttons: Below the hero, full-width row, scroll if overflow
- Summary cards: Single column, stacked
- Repository URL: Truncated with copy button

#### Desktop (`min-width: 1024px`)

```
┌─────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────┐ │
│  │  ← Back                                         │ │
│  │  [BACKEND]  ● Passed                            │ │
│  │  Project Name                  [Edit] [Export]   │ │
│  │  📍 git@gitlab.com:ns/proj.git                   │ │
│  └──────────── HERO GRADIENT ──────────────────────┘ │
│                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ Quality Gate  │ │ Deployments  │ │  Team        │ │
│  │ ✓ Passed      │ │ ● Dev: ON    │ │ @john (M)    │ │
│  │ Coverage: 85% │ │ ● Stg: ON    │ │ @jane (D)    │ │
│  │ Dupl: 5.1%    │ │ ○ Prod: OFF  │ │ @bob  (R)    │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ │
│                                                     │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Description                                     │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

- Hero: Full height (`200px`), title at `36px`, actions on hero top-right
- Summary cards: `grid-template-columns: repeat(3, 1fr)`
- Description: Full-width card below

### 9.5 Grid System (Mobile-First)

All grids start at **1 column** and expand upward.

```css
/* Base: mobile */
.kpi-grid       { grid-template-columns: repeat(2, 1fr); gap: var(--space-3); }
.card-grid      { grid-template-columns: 1fr; gap: var(--space-4); }
.summary-grid   { grid-template-columns: 1fr; gap: var(--space-4); }

/* sm (640px) */
@media (min-width: 640px) {
  .card-grid    { grid-template-columns: repeat(2, 1fr); }
}

/* md (768px) */
@media (min-width: 768px) {
  .kpi-grid     { grid-template-columns: repeat(4, 1fr); }
}

/* lg (1024px) */
@media (min-width: 1024px) {
  .card-grid    { grid-template-columns: repeat(3, 1fr); }
  .summary-grid { grid-template-columns: repeat(3, 1fr); }
}

/* xl (1280px) */
@media (min-width: 1280px) {
  .card-grid    { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
}
```

---

## 10. Iconography

Use a consistent icon set. Recommended: [Lucide Icons](https://lucide.dev/) (MIT licensed, clean, consistent).

### Key Icons

| Element | Icon | Size |
|---------|------|------|
| Dashboard nav | `LayoutDashboard` | 20px |
| Projects nav | `FolderKanban` | 20px |
| New Project | `Plus` | 20px |
| Reports nav | `BarChart3` | 20px |
| Settings nav | `Settings` | 20px |
| Repository URL | `GitBranch` | 16px |
| Copy | `Copy` / `Check` | 16px |
| Calendar / Date | `Calendar` | 14px |
| Quality Gate OK | `ShieldCheck` | 20px |
| Quality Gate Error | `ShieldX` | 20px |
| Online | `CircleDot` | 14px |
| Offline | `CircleX` | 14px |
| User / Member | `User` | 16px |
| Logout | `LogOut` | 18px |
| Trash / Remove | `Trash2` | 16px |
| Add member | `PlusCircle` | 16px |
| Back | `ArrowLeft` | 18px |
| Chevron (select) | `ChevronDown` | 16px |
| Close | `X` | 18px |
| Search | `Search` | 16px |
| Loading spinner | `Loader2` (animated) | 20px |
| Error alert | `AlertTriangle` | 20px |
| Success | `CheckCircle2` | 20px |
| Backend type | `Server` | 18px |
| Frontend type | `Monitor` | 18px |
| Export | `Download` | 18px |
| Edit | `Pencil` | 16px |
| View | `Eye` | 16px |
| Approve | `Check` | 16px |
| Reject | `X` | 16px |
| Grid view | `LayoutGrid` | 18px |
| Table view | `List` | 18px |
| Help | `HelpCircle` | 18px |
| Hamburger | `Menu` | 20px |

---

## 11. Motion & Transitions

Keep animations subtle and functional. We use the **`motion`** library (v12+) for JS-driven animations and CSS transitions for simple hover/focus states.

### 11.1 CSS Transitions (hover, focus)

| Property | Duration | Easing | Usage |
|----------|----------|--------|-------|
| Background, border, color | `150ms` | `ease-in-out` | Hover states, focus |
| Skeleton shimmer | `1500ms` | `linear` | Loading placeholders |
| Sidebar collapse/expand | `200ms` | `ease-in-out` | Width transition |

### 11.2 Motion Library Animations

Import pattern: `import * as m from "motion/react-client"` (client components).
For `AnimatePresence` (exit animations): `import { AnimatePresence } from "motion/react"`.

| Component | Animation | Duration | Details |
|-----------|-----------|----------|---------|
| Login card | Fade up + scale | `400ms` | `opacity: 0→1, y: 20→0, scale: 0.97→1` |
| Login logo | Spring pop | spring | `scale: 0→1`, delay 200ms |
| Project cards (list) | Staggered fade up | `300ms` | `y: 16→0`, stagger `50ms` per card |
| Projects page header | Fade down | `300ms` | `y: -8→0` |
| Project hero | Fade down | `400ms` | `y: -10→0` |
| Modal overlay | Fade | `200ms` | `opacity: 0→1` with exit |
| Modal content | Scale + fade | `200ms` | `scale: 0.95→1, y: 10→0` with exit |
| Toast | Slide up + scale | `250ms` | `y: 20→0, scale: 0.95→1`, reverse on exit |
| Empty state | Fade up | `350ms` | `y: 12→0`, icon spring pop |
| Create success/error | Scale + fade | `350ms` | Icon spring pop (delay 150ms) |

- Card hover: CSS `transform: translateY(-2px)` + `--shadow-lg`
- No page transition animations for v1

---

## 12. Responsive Breakpoints (Mobile-First)

All base styles are written for **mobile** (`320px`+). Use **`min-width`** media queries to progressively enhance for larger screens. Never use `max-width` queries.

```css
/* Base: mobile (320px+) — no media query needed */
.card-grid { grid-template-columns: 1fr; }

/* Tablet and up */
@media (min-width: 768px) { ... }

/* Desktop and up */
@media (min-width: 1280px) { ... }

/* Large desktop and up */
@media (min-width: 1440px) { ... }
```

| Token | Query | What changes |
|-------|-------|-------------|
| *(base)* | `< 768px` | Single column layout. Sidebar hidden behind hamburger menu. Full-width cards stacked vertically. KPI row scrolls horizontally or stacks 2x2. Bottom nav optional. Touch-friendly tap targets (min 44px). |
| `--bp-sm` | `min-width: 640px` | Slightly wider cards. 2-column project card grid possible. |
| `--bp-md` | `min-width: 768px` | Collapsed sidebar (icon-only, 64px). 2-column KPI row. 2-column project cards. Table view becomes available. |
| `--bp-lg` | `min-width: 1024px` | Expanded sidebar (240px). 3-column project cards. Summary cards go side-by-side (3 columns). |
| `--bp-xl` | `min-width: 1280px` | Full layout. 4-column KPI row. 3-4 column card grid. Content max-width `1440px`. |
| `--bp-2xl` | `min-width: 1440px` | Extra breathing room. 4-column card grid. Wider content area. |

### 12.1 Mobile-First Checklist

When implementing any component, verify:

- [ ] Component renders correctly at `320px` wide (base)
- [ ] Touch targets are at least `44px × 44px`
- [ ] Text is readable without horizontal scrolling
- [ ] Cards stack vertically by default
- [ ] Tables become horizontally scrollable or switch to card-list on mobile
- [ ] Modals become full-screen (or near full-screen) on mobile
- [ ] The hero banner reduces height and font size on mobile
- [ ] Filter chips row scrolls horizontally on overflow (no wrapping)
- [ ] KPI cards stack 2x2 or scroll horizontally on mobile
- [ ] Navigation is accessible via hamburger menu on mobile

---

## 13. Footer

> See reference image 2.8.

- Background: `--color-white`
- Border-top: `1px solid --color-neutral-200`
- Padding: `--space-6 --space-8`
- **Left:** App name + copyright text (`--text-small`, `--color-neutral-500`)
- **Center:** Social media icon links (20px, `--color-neutral-500`, hover `--color-neutral-700`)
- **Right:** Version indicator — green dot (8px) + "v1.0" (`--text-small`, `--color-neutral-500`)

---

## 14. Dark Mode (Future — v2)

Reserve CSS custom property tokens for a future dark theme. All colors should be referenced via tokens, never hardcoded. Example future mapping:

| Token | Light | Dark (planned) |
|-------|-------|----------------|
| `--color-bg-page` | `#FAFAFA` | `#0A0A0A` |
| `--color-bg-card` | `#FFFFFF` | `#171717` |
| `--color-bg-hero` | `#1B2559 → #2563EB` | `#0F172A → #1E40AF` |
| `--color-text-primary` | `#0A0A0A` | `#FAFAFA` |
| `--color-text-secondary` | `#404040` | `#A3A3A3` |
| `--color-border` | `#E5E5E5` | `#2E2E2E` |
