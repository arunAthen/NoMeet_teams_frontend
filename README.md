# NoMeet Teams Frontend 🚀
> Autonomous Delivery & Operations Copilot for Microsoft Teams

`NoMeet` eliminates status meetings by autonomously syncing with Teams files, tracking Change Requests (CRs), resolving bugs, and providing real-time delivery intelligence right inside Microsoft Teams.

---

## 📁 Repository Structure
```
NoMeet_teams_frontend/
├── index.html                  # Main Teams Tab Cockpit interface
├── style.css                   # Teams-native styling (Fluent UI inspired)
├── app.js                      # Cockpit logic & dynamic multi-group workspace switcher
├── config.js                   # Backend API connection settings
├── README.md                   # Frontend documentation
├── .gitignore                  # Git ignore rules
└── teams_package/
    ├── manifest.json           # Microsoft Teams App Manifest (v1.16)
    ├── color.png               # 192x192 App icon
    ├── outline.png             # 32x32 Monochrome icon
    ├── build_teams_zip.py      # Zip builder script
    └── teams_365_agent.zip     # Ready-to-upload Teams package
```

---

## ⚙️ Configuration (`config.js`)
By default, the frontend connects to your deployed Vercel backend:
```javascript
window.CONFIG = {
  API_BASE_URL: "https://teams-365-agent-v5ge.vercel.app"
};
```
If you deploy the backend to your own domain or Azure App Service, update `API_BASE_URL` in `config.js`.

---

## 📦 How to Sideload into Microsoft Teams

1. Locate the package: `teams_package/teams_365_agent.zip`.
2. Open **Microsoft Teams** (web or desktop).
3. In the left navigation, click **Apps** (`...` or grid icon).
4. Click **Manage your apps** (bottom-left) -> **Upload an app** -> **Upload a custom app**.
5. Select `teams_365_agent.zip`.
6. Click **Add** — NoMeet will appear in your sidebar and personal apps!

---

## 🌐 Deploying Frontend (Optional)
This frontend is 100% static (HTML/CSS/JS) and can be hosted on:
- **Vercel** (`vercel deploy`)
- **GitHub Pages**
- **Azure Static Web Apps**
- **Or served directly from the backend** via `/teams/tab`
