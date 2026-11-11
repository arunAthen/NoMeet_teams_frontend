# NoMeet — Teams Frontend & App Package

This repository contains the Microsoft Teams Tab UI and the official Microsoft Teams App Package for the **NoMeet M365 Delivery Intelligence Copilot**.

## Structure
* `index.html` — The Delivery & Operations Cockpit interface
* `style.css` — Microsoft Teams Fluent UI dark/light theme
* `app.js` — Teams JS SDK integration, multi-workspace routing, and chat stream
* `config.js` — Backend API URL configuration
* `teams_package/` — Official Microsoft Teams app package:
  * `manifest.json` — Teams app manifest configuration
  * `color.png` & `outline.png` — App icons
  * `build_teams_zip.py` — Script to package `teams_365_agent.zip`
  * `teams_365_agent.zip` — Ready-to-upload Teams package

## Configuration
When deploying the frontend to a separate host (Azure Static Web Apps, Vercel, S3/CloudFront), open `config.js` and set your backend URL:
```javascript
window.CONFIG = {
  API_BASE_URL: "https://your-backend.azurewebsites.net"
};
```

## How to Build the Teams Package
```powershell
python teams_package/build_teams_zip.py
```
This generates `teams_package/teams_365_agent.zip` which you upload directly to the **Microsoft Teams Admin Center** or **Teams App Store**.
