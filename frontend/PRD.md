# Product Requirements Document (PRD)

## Carli — CI/CD & Project Orchestration Platform

**Version:** 1.0
**Last Updated:** 2026-02-07

---

## 1. Product Overview

Carli is an internal platform that automates the creation, monitoring, and incident management of software projects. It orchestrates GitLab, SonarQube, Logfire, Jira, and Gemini AI into a single dashboard where Project Managers and Admins can spin up fully configured repositories, monitor code quality and deployment health, and automatically triage production errors into Jira tickets using AI.

### 1.1 Target Users

| Role | Description | Permissions |
|------|-------------|-------------|
| **Admin** | Full platform access — manages users, roles, and all projects | `create_project`, `read_project`, `read_projects` |
| **Project Manager (PM)** | Creates and monitors their own projects | `create_project`, `read_project`, `read_projects` |

### 1.2 Core Value Proposition

- **One-click project bootstrapping** — creates a GitLab repo, SonarQube project, Logfire monitoring, protected branches, and team access in a single action.
- **Unified project overview** — code quality, team members, and deployment health in one screen.
- **AI-powered incident management** — production errors are automatically analyzed and turned into actionable Jira tickets.

---

## 2. Authentication & Session Management

### 2.1 Login

| Field | Type | Validation |
|-------|------|------------|
| Email | `string` | Required, valid email format |
| Password | `string` | Required, min 8 characters |

**API:** `POST /auth/login`
**Request:** `application/x-www-form-urlencoded` (OAuth2 form: `username` = email, `password`)
**Response:**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```
The server also sets an `access_token` **HTTPOnly Secure cookie** (duration: 30 min).

**Error States:**

| Scenario | HTTP Status | Message |
|----------|-------------|---------|
| Invalid email or password | `401` | "Could not validate credentials" |
| Missing fields | `422` | Validation error details |

**Frontend Requirements:**
- Login form with email and password fields.
- "Log in" submit button.
- Display inline validation errors under each field.
- On success, redirect to the **Projects List** page.
- On `401`, show a toast/banner: "Invalid email or password".
- Store the token from the response body for the `Authorization: Bearer <token>` header on all subsequent requests. The cookie is also sent automatically.

### 2.2 Logout

**API:** `POST /auth/logout`
**Response:** `204 No Content` — deletes the `access_token` cookie.

**Frontend Requirements:**
- Logout button/option accessible from the main layout (e.g., header avatar dropdown).
- On click, call the endpoint, clear any local token storage, and redirect to the Login page.

### 2.3 Session Expiration

- Tokens expire after **30 minutes**.
- When any API call returns `401`, redirect the user to Login with a message: "Session expired. Please log in again."

---

## 3. Projects

### 3.1 Projects List Page

Displays all projects owned by the current user.

**API:** `GET /projects/`
**Auth:** Requires `read_projects` permission.
**Response:**
```json
[
  {
    "id": "uuid",
    "name": "my-project",
    "url_repository": "git@gitlab.example.com:namespace/my-project.git",
    "created_at": "2026-01-15T10:30:00Z"
  }
]
```

**Frontend Requirements:**
- Display a list/grid of project cards.
- Each card shows:
  - **Project name** (prominent).
  - **Repository URL** (monospace, with a copy-to-clipboard button).
  - **Created date** (formatted relative or absolute, e.g., "Jan 15, 2026").
- A **"New Project"** button (visible only if user has `create_project` permission) that opens the Create Project flow.
- Clicking a project card navigates to the **Project Overview** page.
- **Empty state:** When no projects exist, show an illustration with "No projects yet" and a CTA to create one.
- **Loading state:** Skeleton cards while fetching.

### 3.2 Create Project

A multi-section form to bootstrap a new project.

**API:** `POST /projects/`
**Auth:** Requires `create_project` permission.
**Request:**
```json
{
  "name": "my-new-project",
  "description": "Optional project description",
  "project_type": "backend",
  "members": [
    {
      "gitlab_user_name": "john.doe",
      "role": "maintainer"
    },
    {
      "gitlab_user_name": "jane.smith",
      "role": "developer"
    }
  ]
}
```

**Response (201):**
```json
{
  "repo_url": "git@gitlab.example.com:namespace/my-new-project.git",
  "project_id": "uuid"
}
```

#### 3.2.1 Form Fields

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| Project Name | `text` | Yes | Non-empty, alphanumeric + hyphens | Will be slugified (e.g., "My Project" → "my-project") |
| Description | `textarea` | No | Max 500 chars | Brief project description |
| Project Type | `select` | Yes | `backend` or `frontend` | Determines the template used for repository bootstrapping |
| Team Members | `dynamic list` | No | At least `gitlab_user_name` and `role` per entry | Users can add/remove member rows |

#### 3.2.2 Team Members Sub-form

Each member row contains:

| Field | Type | Options | Notes |
|-------|------|---------|-------|
| GitLab Username | `autocomplete text` | Search GitLab users | See section 3.2.3 |
| Role | `select` | `developer`, `maintainer`, `reporter` | Maps to GitLab access levels |

- An **"Add Member"** button appends a new empty row.
- Each row has a **remove** (trash icon) button.
- Minimum 0 members, no explicit maximum.

#### 3.2.3 GitLab User Search (for member autocomplete)

> **Note:** There is no dedicated search endpoint exposed in the backend yet. The frontend should implement an autocomplete that works with a future endpoint or, for v1, use a simple text input for the GitLab username. The backend validates the username during project creation.

#### 3.2.4 What Happens on Submit

The backend performs **16 steps** in sequence (takes ~10-30 seconds):

1. Creates a GitLab project (private).
2. Generates and commits project template files (README, Dockerfile, CI config, etc.).
3. Creates a `develop` branch.
4. Protects `main`, `develop`, `release/*`, and `hotfix/*` branches.
5. Adds team members with appropriate access levels.
6. Creates a SonarQube project + analysis token.
7. Binds SonarQube to GitLab (for MR decoration).
8. Creates a Logfire project + write token.
9. Creates a Logfire webhook channel + error alert.
10. Saves the project to the database.

**If any step fails**, the backend rolls back (deletes GitLab project, SonarQube project) and returns `500`.

**Frontend Requirements:**
- On submit, show a **full-page or modal loading state** with a progress message (e.g., "Setting up your project..."). This operation is not instant.
- Disable the form while the request is in-flight.
- **On success (201):**
  - Show a success screen with:
    - "Project created successfully!"
    - The **repository SSH URL** (monospace, copy-to-clipboard).
    - A button: "Go to Project" → navigates to Project Overview.
    - A button: "Create Another" → resets the form.
- **On error (500):**
  - Show an error message: "Failed to create project. Please try again or contact support."
  - Keep the form data so the user doesn't lose their input.
- **On validation error (422):**
  - Show inline field-level errors.

### 3.3 Project Overview Page

A dashboard view for a single project aggregating data from multiple sources.

**API:** `GET /projects/{project_id}`
**Auth:** Requires `read_projects` permission. User must own the project.
**Response:**
```json
{
  "id": "uuid",
  "name": "my-project",
  "url_repository": "git@gitlab.example.com:namespace/my-project.git",
  "created_at": "2026-01-15T10:30:00Z",
  "quality_gate": {
    "status": "OK",
    "conditions": [
      {
        "status": "OK",
        "metric_key": "new_coverage",
        "comparator": "LT",
        "error_threshold": "80.0",
        "actual_value": "85.3"
      },
      {
        "status": "ERROR",
        "metric_key": "new_duplicated_lines_density",
        "comparator": "GT",
        "error_threshold": "3.0",
        "actual_value": "5.1"
      }
    ]
  },
  "members": [
    {
      "id": 1,
      "username": "john.doe",
      "name": "John Doe",
      "state": "active",
      "access_level": 40
    }
  ],
  "stages": [
    { "stage": "development", "is_ready": true },
    { "stage": "staging", "is_ready": true },
    { "stage": "production", "is_ready": false }
  ]
}
```

**Error States:**

| Scenario | HTTP Status | Message |
|----------|-------------|---------|
| Project not found or not owned | `404` | "Project not found" |
| Integration failure | `500` | Error message |

#### 3.3.1 Page Sections

The Project Overview page should be composed of the following sections:

---

**A. Header**

- **Project name** (large heading).
- **Repository URL** (monospace, copy-to-clipboard icon).
- **Created date** (e.g., "Created on Jan 15, 2026").
- **Back link** to Projects List.

---

**B. Quality Gate Card**

Displays SonarQube quality gate status.

- **Overall status badge:**
  - `OK` → Green badge: "Passed"
  - `WARN` → Yellow badge: "Warning"
  - `ERROR` → Red badge: "Failed"
- **Conditions list** — each condition as a row:
  - Metric name (humanized from `metric_key`):
    - `new_coverage` → "Coverage"
    - `new_duplicated_lines_density` → "Duplicated Lines"
    - `new_reliability_rating` → "Reliability"
    - `new_security_rating` → "Security"
    - `new_maintainability_rating` → "Maintainability"
    - Others → Title-case the key with underscores replaced by spaces
  - **Actual value** (bold).
  - **Threshold** (e.g., "≥ 80%" or "≤ 3%", derived from `comparator` + `error_threshold`):
    - `LT` → "≥ {threshold}" (error when less than)
    - `GT` → "≤ {threshold}" (error when greater than)
  - **Status indicator:** green check / yellow warning / red cross.

---

**C. Deployment Stages Card**

Shows the health of each environment.

- Three rows/columns, one per stage: **Development**, **Staging**, **Production**.
- Each stage shows:
  - **Stage name** with an environment-specific icon or color.
  - **Status:**
    - `is_ready: true` → Green dot + "Online"
    - `is_ready: false` → Red dot + "Offline"
- If no `web_domain` is set, show: "No domain configured" with a neutral indicator.

---

**D. Team Members Card**

Lists all GitLab members of the project.

- Table or list with columns:
  - **Name** (or "—" if empty).
  - **Username** (prefixed with `@`).
  - **Role** (derived from `access_level`):
    - `50` → "Owner"
    - `40` → "Maintainer"
    - `30` → "Developer"
    - `20` → "Reporter"
    - `10` → "Guest"
  - **Status:** `active` → green dot, `blocked` → red dot.

---

#### 3.3.2 Loading & Error States

- **Loading:** Show skeleton placeholders for each card.
- **Partial failure:** If one integration fails, the backend may still return partial data or `500`. If `500`, show a full-page error with a "Retry" button.

---

## 4. Webhook-Driven Features (Background / No Direct UI)

### 4.1 Automated Incident Triage

When a production error occurs in a monitored project:

1. **Logfire** detects an error-level log and fires a webhook to the backend.
2. The backend sends the error context (message, stack trace, request data) to **Gemini AI**.
3. Gemini generates a structured Jira ticket (summary + description).
4. The backend creates a **Jira Bug issue** automatically.

**Frontend Requirements:**
- No direct UI interaction needed for this flow.
- **Future consideration:** A "Recent Incidents" section on the Project Overview page that lists recent Jira tickets created from alerts. (Not currently supported by the API.)

---

## 5. Navigation & Layout

### 5.1 Application Shell

The app should have a consistent shell/layout:

- **Sidebar or Top Navigation:**
  - Logo / App name ("Carli").
  - Navigation link: **Projects** (leads to Projects List).
  - Future: more nav items (Users, Settings, etc.).
- **Header (if top-bar):**
  - Breadcrumbs (e.g., Projects > my-project).
  - User avatar/name with dropdown:
    - Profile (future).
    - Logout.
- **Content Area:**
  - Renders the active page.

### 5.2 Route Structure

| Route | Page | Auth Required |
|-------|------|---------------|
| `/login` | Login | No |
| `/projects` | Projects List | Yes |
| `/projects/new` | Create Project | Yes (`create_project`) |
| `/projects/:id` | Project Overview | Yes (`read_project`) |

### 5.3 Auth Guards

- All routes except `/login` require authentication.
- If a user accesses a protected route without a valid token, redirect to `/login`.
- If a user accesses a route requiring a permission they don't have, show a "403 — Access Denied" page.

---

## 6. API Reference Summary

| Method | Endpoint | Description | Auth Scope |
|--------|----------|-------------|------------|
| `POST` | `/auth/login` | Authenticate user | None |
| `POST` | `/auth/logout` | End session | Authenticated |
| `GET` | `/projects/` | List user's projects | `read_projects` |
| `POST` | `/projects/` | Create new project | `create_project` |
| `GET` | `/projects/{id}` | Project overview | `read_projects` |
| `GET` | `/health` | Health check | None |
| `POST` | `/webhooks/logfire/alerts` | Receive Logfire alert | None (webhook) |

### 6.1 Common Response Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (logout, webhook ack) |
| `401` | Unauthorized — invalid/expired token |
| `403` | Forbidden — insufficient permissions |
| `404` | Not Found — resource doesn't exist or not owned |
| `422` | Validation Error — invalid request body |
| `500` | Internal Server Error — integration failure |
| `502` | Bad Gateway — Jira/AI service failure |

### 6.2 Authentication Header

All authenticated requests should include:
```
Authorization: Bearer <access_token>
```
The backend also reads from the `access_token` cookie.

---

## 7. Data Types & Enums

### 7.1 Project Type

```
"backend" | "frontend"
```

### 7.2 Member Roles (for project creation form)

```
"developer" | "maintainer" | "reporter"
```

### 7.3 GitLab Access Levels (displayed in overview)

| Value | Label |
|-------|-------|
| `10` | Guest |
| `20` | Reporter |
| `30` | Developer |
| `40` | Maintainer |
| `50` | Owner |

### 7.4 Quality Gate Status

```
"OK" | "WARN" | "ERROR"
```

### 7.5 Environment / Stage

```
"development" | "staging" | "production"
```

---

## 8. Non-Functional Requirements

### 8.1 Performance

- **Projects List** should load in < 1 second.
- **Project Overview** may take 2-5 seconds (aggregates data from GitLab + SonarQube + health checks). Show loading indicators.
- **Create Project** takes 10-30 seconds. Must show progress/loading state.

### 8.2 Responsive Design (Mobile-First)

The frontend must be built with a **mobile-first** approach: base CSS targets the smallest viewport (`320px`+), and complexity is added progressively via `min-width` media queries.

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Base (mobile) | `< 640px` | Single column, no sidebar (hamburger drawer), stacked cards, full-width inputs |
| `sm` | `≥ 640px` | 2-column card grid possible |
| `md` | `≥ 768px` | Collapsed sidebar (icon-only), table view available, 2-col KPI |
| `lg` | `≥ 1024px` | Expanded sidebar (240px), 3-column cards, 3-column summary |
| `xl` | `≥ 1280px` | 4-column KPI, full desktop layout |
| `2xl` | `≥ 1440px` | Extra wide content area |

**Key mobile requirements:**
- All touch targets minimum `44px × 44px`
- Filter chips scroll horizontally on overflow
- Tables hidden on mobile — card-list view only
- Modals become bottom sheets or near full-screen
- Hero banner reduces height and font size
- Action buttons stack below hero instead of overlaying it

### 8.3 Browser Support

- Chrome (latest 2 versions).
- Firefox (latest 2 versions).
- Edge (latest 2 versions).

### 8.4 Accessibility

- WCAG 2.1 AA compliance.
- Keyboard navigable.
- Screen reader friendly (ARIA labels on interactive elements).
- Sufficient color contrast (4.5:1 for text).

---

## 9. Future Considerations (Out of Scope for v1)

These features are **not** currently supported by the backend but are anticipated:

1. **User Management** — CRUD for users, role assignment.
2. **Project Settings** — edit project details, add/remove members after creation, configure `web_domain`.
3. **Incident Feed** — display recent Jira tickets created from Logfire alerts.
4. **CI/CD Pipeline Viewer** — show GitLab pipeline status in the overview.
5. **Notifications** — in-app alerts for failed quality gates or deployment failures.
6. **Dashboard / Analytics** — aggregate metrics across all projects.
7. **Dark Mode** — toggle between light and dark themes.
