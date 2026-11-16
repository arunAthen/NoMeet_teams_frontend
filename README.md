# NoMeet Teams Frontend 🚀
> Native Microsoft Teams Tab & Cockpit Interface (Vanilla ES6 + Teams JS SDK v2.19)

[![Teams App Version](https://img.shields.io/badge/Manifest%20Version-1.0.2-blue)](teams_package/manifest.json)
[![Supported Scopes](https://img.shields.io/badge/Scopes-Personal%20%7C%20Team%20%7C%20GroupChat-success)](teams_package/manifest.json)
[![Live Backend](https://img.shields.io/badge/Connected%20Backend-Vercel%20Live-brightgreen)](https://no-meet-teams-backend.vercel.app)

`NoMeet` eliminates status meetings by autonomously syncing with Teams files, tracking Change Requests (CRs), resolving bugs, and providing real-time delivery intelligence right inside Microsoft Teams.

---

## 📁 Repository Structure

```
NoMeet_teams_frontend/
├── index.html                  # Main Teams Tab Cockpit interface (Fluent UI layout)
├── style.css                   # Teams-native styling (Dark & light theme support)
├── app.js                      # Core frontend logic, user privacy, & local persistence
├── config.js                   # Backend API connection settings
├── README.md                   # Frontend documentation
├── .gitignore                  # Git ignore rules
└── teams_package/
    ├── manifest.json           # Microsoft Teams App Manifest (v1.16, package v1.0.2)
    ├── color.png               # 192x192 official Teams app icon
    ├── outline.png             # 32x32 transparent monochrome navigation icon
    ├── build_teams_zip.py      # Automated package packaging script
    └── teams_365_agent.zip     # Ready-to-upload Teams package (v1.0.2)
```

---

## 🌟 Key Architecture & Capabilities

1. **Strict User Privacy & Personal Bot Isolation:**
   - Automatically extracts authenticated user metadata from Microsoft Teams JS SDK (`context.user.id`, `context.user.userPrincipalName`, `context.user.displayName`).
   - Every session is tagged and filtered by `user_id`. Even when multiple team members use the same tab in a shared group chat, each person's chat history is strictly isolated and confidential.

2. **Dual-Layer Persistence (Offline-First):**
   - Implements local storage caching (`localStorage`) for sessions and messages.
   - UI renders with **0ms latency** on load, eliminating chat loss or loading delays across serverless container recycling.

3. **Multi-Scope Tab Support:**
   - **Personal Tab (`staticTabs`):** Full standalone delivery cockpit in the Teams sidebar.
   - **Group Chat & Team Channels (`configurableTabs`):** Supports 1-click addition into any team or group conversation via `microsoftTeams.pages.config.registerOnSaveHandler`.

4. **Dynamic Workspace Discovery:**
   - Automatically detects active chat or channel IDs and registers them via `POST /api/v1/teams/groups/register`.
   - Decodes messy URL-encoded thread IDs into clean human-readable names.

---

## 📦 How to Sideload into Microsoft Teams

1. Locate the package file:  
   👉 **`teams_package/teams_365_agent.zip`**
2. Open **Microsoft Teams** (desktop client or browser).
3. In the left navigation rail, click **Apps** -> **Manage your apps** -> **Upload an app** -> **Upload a custom app**.
4. Select `teams_365_agent.zip`.
5. Click **Add** to install it into your personal workspace, or choose **Add to a team / chat** to embed it in a project conversation.

---

## ⚙️ Configuration (`config.js`)

The frontend connects to the production Vercel backend:
```javascript
window.CONFIG = {
  API_BASE_URL: "https://no-meet-teams-backend.vercel.app"
};
```
If deploying to a custom domain or staging backend, update `API_BASE_URL` accordingly.
