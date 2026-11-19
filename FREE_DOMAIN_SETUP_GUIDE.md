# FactoryMind AI — Free Domain & Public Access Guide

This guide explains how to get a **100% Free Domain** with automated **HTTPS SSL** for **FactoryMind AI**.

---

## ⚡ Method 1: Instant Free Public Domain (Zero Setup - Runs from your PC)

You can generate an active, public HTTPS domain in 5 seconds to present to college professors, examiners, or access on mobile devices without any cloud hosting or payment.

### How to Run:
Double-click:
```cmd
run_free_domain.bat
```
*(Or select option `[6]` inside `start_all.bat`)*

### Providers Available in the Launcher:
1. **Cloudflare Quick Tunnel (Recommended):**
   - **Domain:** `https://<random-unique-words>.trycloudflare.com`
   - **Cost:** 100% Free, Zero Signup, No Credit Card.
   - **Features:** Enterprise-grade Cloudflare SSL, high-speed worldwide CDN, full WebSocket support.
2. **Localhost.run (Built-in Windows SSH):**
   - **Domain:** `https://<unique-id>.lhr.life`
   - **Cost:** 100% Free, requires zero downloads.
3. **Pinggy Tunnel:**
   - **Domain:** `https://<random>.a.free.pinggy.link`
4. **ngrok:**
   - **Domain:** `https://<your-subdomain>.ngrok-free.app`

---

## 🌐 Method 2: Permanent 24/7 Free Cloud Hosting & Domain (Render.com)

If you want your platform accessible even when your computer is shut down, you can deploy it to **Render.com** for free.

- **Your Free Domain:** `https://factorymind-ai.onrender.com`
- **Cost:** \$0/month forever.
- **SSL:** Automatic Let's Encrypt HTTPS.

### Steps to Deploy (Takes ~3 minutes):
1. **Push your code to GitHub:**
   - Create a free GitHub repository (e.g. `factorymind-ai`).
   - Push the contents of `C:\Users\Pratiksha\.gemini\antigravity\scratch\factorymind` to your repository.
2. **Deploy on Render:**
   - Go to [https://render.com](https://render.com) and create a free account.
   - Click **"New +"** ➔ **"Web Service"**.
   - Connect your GitHub repository.
   - Set the following fields:
     - **Root Directory:** `backend`
     - **Runtime:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt && python seed_data.py`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** `Free`
3. Click **"Deploy Web Service"**.
   - Render will build your application and assign you a permanent public URL:  
     `https://factorymind-ai.onrender.com`!

---

## 🏷️ Method 3: 100% Free Custom Developer Domain Names

If you want a professional, named subdomain for your portfolio:

| Domain Provider | Example Free Domain | How to Get It |
| :--- | :--- | :--- |
| **is-a.dev** | `https://factorymind.is-a.dev` | 100% free open-source domain for developers. Register via a quick GitHub Pull Request at [is-a.dev](https://is-a.dev). |
| **DuckDNS** | `https://factorymind.duckdns.org` | Free dynamic DNS service with HTTPS support at [duckdns.org](https://www.duckdns.org/). |
| **GitHub Student Pack** | `https://factorymind.me` or `.tech` | If you have a college `.edu` or student email, GitHub gives you a **free 1-year top-level domain** (.me, .tech, or .live) via Namecheap/Name.com. |

---

## 📱 How to Access on Mobile or Other Devices

Once your domain is active (either via `run_free_domain.bat` or Render):
1. Open the generated HTTPS URL on your phone or tablet browser.
2. The UI is fully responsive — you can log in, view the **3D WebGL Digital Twin**, monitor real-time vibration spectrograms, and chat with the **AI Copilot**.
