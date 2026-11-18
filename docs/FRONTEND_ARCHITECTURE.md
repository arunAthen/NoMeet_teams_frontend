# NoMeet Frontend — Technical Architecture & Implementation Specification

> **Component:** Microsoft Teams Tab Client  
> **Repository:** `NoMeet_teams_frontend`  
> **Target Platform:** Microsoft Teams Desktop, Web, iOS/Android Clients (via Teams JS SDK v2.19)  
> **Production Deployment:** `https://no-meet-teams-backend.vercel.app/teams/tab/index.html`  
> **Manifest Version:** `1.0.2`  

---

## 1. Architectural Philosophy & Overview

The NoMeet frontend is built on a **zero-overhead, vanilla-first architectural model**. Unlike standard modern web applications that rely on heavy Node.js runtimes, webpack/vite bundlers, and gigabytes of `node_modules`, NoMeet employs pure HTML5, CSS3, and ES6 JavaScript.

### Why Vanilla ES6 in an Enterprise Teams Tab?
1. **Zero Cold-Start Latency:** In Microsoft Teams, web tabs run inside isolated iframes. Heavy React/Angular client bundles cause noticeable white-screen flashes and several seconds of hydration delay. NoMeet renders in **sub-100 milliseconds**.
2. **Deterministic Sandboxing:** Free from external bundle dependencies that could fail or conflict within Teams webview wrappers.
3. **Fluent Design Alignment:** Implements the official Microsoft Teams Fluent UI design tokens using pure CSS custom properties, adapting seamlessly across desktop, web, and mobile.

---

## 2. Microsoft Teams JS SDK v2.19 Lifecycle

The frontend integrates directly with the official `@microsoft/teams-js` v2.19.0 client library loaded via CDN:
```html
<script src="https://res.cdn.office.net/teams-for-each/teams-client/v2.19.0/js/MicrosoftTeams.min.js"></script>
```

### Complete Lifecycle State Flow

```
                      Browser / Teams Host Loaded
                                   │
                                   ▼
                   `microsoftTeams.app.initialize()`
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
          Running inside Teams           Running Standalone
                     │                           │
                     ▼                           ▼
          `app.notifySuccess()`          Fallback to standard web
                     │                   (generates local user ID)
                     ▼
       `pages.config.registerOnSaveHandler()`
         (Enables 1-click tab pinning)
                     │
                     ▼
           `app.getContext()`
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
      Context      Context     Context
      Identity      Host        Theme
    (User AAD ID) (Chat/Team) (Light/Dark)
         │           │           │
         └───────────┬───────────┘
                     │
                     ▼
       Update Client State Machine
                     │
                     ▼
       Auto-Register Workspace via API
                     │
                     ▼
    Render Dual-Layer Offline-First Cache
```

### Context Extraction
When loaded inside Microsoft Teams, `microsoftTeams.app.getContext()` dynamically extracts:
- **User Identity:**
  - `context.user.id`: Microsoft Entra Object ID (UUID).
  - `context.user.userPrincipalName`: Organizational email (e.g., `devadmin@organization.onmicrosoft.com`).
  - `context.user.displayName`: User's full friendly name.
- **Host Context:**
  - `context.chat.id`: Unique thread ID for 1:1 or Group Chats (`19:...@thread.v2`).
  - `context.channel.id`: Channel identifier for Team Channels (`19:...@thread.tacv2`).
  - `context.team.groupId`: Microsoft 365 Unified Group ID.
- **Theme Adaptation:**
  - `context.app.theme`: Evaluates to `'dark'`, `'contrast'`, or `'default'`. Dynamically assigns `document.body.className = "theme-dark"` or `"theme-default"`.

### Configurable Tab Registration
To enable users to pin NoMeet into any Team Channel or Group Chat, the tab registers the Teams configuration hook:
```javascript
microsoftTeams.pages.config.registerOnSaveHandler((saveEvent) => {
  microsoftTeams.pages.config.setConfig({
    entityId: "noMeetCockpitTab",
    contentUrl: "https://no-meet-teams-backend.vercel.app/teams/tab/index.html",
    websiteUrl: "https://no-meet-teams-backend.vercel.app/teams/tab/index.html",
    suggestedDisplayName: "NoMeet Cockpit"
  });
  saveEvent.notifySuccess();
});
microsoftTeams.pages.config.setValidityState(true);
```

---

## 3. Client-Side State Machine & Privacy Isolation

The application state is managed by four central state variables:

```javascript
let currentUserId = localStorage.getItem("nomeet_user_aad_id") || "";
let currentUserName = localStorage.getItem("nomeet_user_name") || "Team Member";
let currentGroupId = "all";
let currentSessionId = null;
```

### Strict Personal Privacy in Shared Channels
A critical enterprise requirement: when NoMeet is pinned as a shared tab in a 50-person group chat or team channel, **conversations must not leak between coworkers**.
- The frontend extracts the active user's unique AAD ID (`currentUserId`).
- When requesting conversational sessions, the client transmits `?user_id=${currentUserId}`.
- Coworker A inspecting the tab sees only their private threads; Coworker B opening the same tab sees only their own.

---

## 4. Dual-Layer Offline-First Persistence

Because the backend is hosted on serverless compute (Vercel AWS Lambda), the backend's `/tmp` SQLite database can be recycled during cold starts or scaling events. To eliminate any loss of conversation state, the frontend implements an **offline-first local persistence architecture**.

```
                User Action / State Event
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
      Layer 1: LocalStorage       Layer 2: Backend REST API
     (`nomeet_sessions_${uid}`)    (`POST /api/v1/teams/...`)
     (`nomeet_msgs_${sid}`)
              │                           │
              ▼                           ▼
      Instant Render (0ms)        Asynchronous Sync & DB Index
```

### Persistence Helpers
- `getLocalSessions()` / `saveLocalSessions(list)`: Reads and writes session metadata per `currentUserId`.
- `getLocalMessages(sessionId)` / `saveLocalMessages(sessionId, msgs)`: Stores full conversation history including citations, evidence steps, and evaluation scores.
- **Reconciliation:** On page load, `loadSessions()` queries both local cache and backend API, deduplicates them by `session_id`, sorts chronologically, and saves the reconciled list back to local storage.

---

## 5. CSS Design System & Fluent UI Tokens

The design system strictly adheres to Microsoft Teams' Fluent Design specifications.

### CSS Custom Properties (`style.css`)
```css
:root, .theme-default {
  --bg-app: #f5f5f7;
  --bg-sidebar: #1e1e24;
  --bg-surface: #ffffff;
  --text-main: #242424;
  --text-muted: #616161;
  --border-color: #e0e0e0;
  --primary: #5b5fc7;        /* Official Teams Blurple */
  --primary-hover: #4f52b2;
  --chat-bubble-user: #e8ebfa;
  --chat-bubble-agent: #ffffff;
}

.theme-dark {
  --bg-app: #141414;
  --bg-sidebar: #1e1e24;
  --bg-surface: #1f1f1f;
  --text-main: #f5f5f5;
  --text-muted: #a6a6a6;
  --border-color: #2d2d2d;
  --primary: #7f85f5;
  --primary-hover: #9297f7;
  --chat-bubble-user: #2d325a;
  --chat-bubble-agent: #252528;
}
```

### Rich Citation & Status Rendering (`formatContent`)
Raw Markdown text returned from the backend agent is dynamically parsed into styled enterprise elements:
- **Document Citations:** `[Doc: Specification Name]` $\rightarrow$ `<span class="badge-tag badge-doc">📄 [Doc: ...]</span>`
- **Teams Chat Citations:** `[Teams: Sender @ Date]` $\rightarrow$ `<span class="badge-tag badge-teams">💬 [Teams: ...]</span>`
- **Ticket / Tracker Citations:** `[Tracker: Ticket ID]` $\rightarrow$ `<span class="badge-tag badge-tracker">📋 [Tracker: ...]</span>`
- **Lifecycle Status Pills:** `Implemented`, `In Progress`, `Blocked` $\rightarrow$ Color-coded status pills.

---

## 6. UI Component Hierarchy & DOM Structure

```
index.html
├── `<aside class="sidebar">`
│   ├── `.brand-header`: Teams icon, App title, Status pill
│   ├── `.user-badge`: Dynamic avatar (initials) + User display name + Privacy indicator
│   ├── `.workspace-selector`: Dropdown for switching between "All Workspaces" and specific group chats/channels
│   ├── `.sidebar-section-header`: Recent Conversations header + "Only You" security badge
│   ├── `#sessionsList`: Scrollable container rendering `.session-card` items
│   └── `#newSessionBtn`: "+ New Conversation" action button
│
└── `<main class="main-content">`
    ├── `<header class="top-bar">`
    │   ├── `#activeWorkspaceName`: Real-time breadcrumb of current project context
    │   └── `.metrics-strip`: Live KPI counters
    │       ├── `#crMetric`: Total Change Requests
    │       ├── `#bugMetric`: Total Active Bugs
    │       ├── `#msgMetric`: Indexed Communications
    │       └── `#specMetric`: Verified Specifications
    │
    ├── `<section class="chat-area">`
    │   └── `#chatViewport`: Scrollable message history rendering `.message-wrapper`
    │       ├── `.message-wrapper.user`
    │       └── `.message-wrapper.assistant`
    │           ├── `.bubble`: Formatted text & citations
    │           ├── `.tool-steps-box`: `<details>` container showing ReAct evidence steps
    │           └── `.eval-row`: Badges displaying Faithfulness, Relevancy, and Groundedness
    │
    └── `<footer class="input-area">`
        ├── `.chips-row`: Quick suggestion prompts
        └── `<form id="chatForm">`
            ├── `#chatInput`: Auto-expanding query input
            └── `#sendBtn`: Submit button with send glyph
```

---

## 7. Security & Iframe Framing Rules

Because Microsoft Teams embeds tabs inside sandboxed iframes, the frontend complies with strict framing controls:
1. **Frame Ancestor Policy:** The backend issues `Content-Security-Policy: frame-ancestors https://teams.microsoft.com https://*.teams.microsoft.com https://*.skype.com https://*.microsoft.com;`
2. **Clickjacking Defense:** Standalone rendering outside of authorized Microsoft domains or localhost development is strictly restricted.
3. **DOM Sanitization:** All incoming user input and assistant text strings pass through `replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")` prior to regex token badge transformation, preventing arbitrary XSS execution.
