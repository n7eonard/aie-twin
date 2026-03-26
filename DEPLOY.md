# AIE Twin — Deployment Guide
## Cloudflare Pages (frontend) + Railway (Starlette backend)

---

## Architecture

```
Browser → Cloudflare Pages (index.html)
             └─ POST /api/chat ──→ Railway (backend/main.py)
                                       └─ Anthropic API
```

The frontend calls your Railway backend. The backend holds the `ANTHROPIC_KEY`
server-side — users never see it.

---

## Step 1 — Deploy the backend to Railway

### 1.1 Create project

1. Go to [railway.app](https://railway.app) → **New Project**
2. Choose **Deploy from GitHub repo**
3. Connect your repo (push this folder to GitHub first if needed)
4. Railway auto-detects Python via `nixpacks.toml` and `Procfile`

### 1.2 Set environment variables

In Railway → your service → **Variables**, add:

| Variable | Value |
|---|---|
| `ANTHROPIC_KEY` | `sk-ant-...` (your key) |
| `ALLOWED_ORIGINS` | `https://your-app.pages.dev` (fill in after step 2) |
| `ALLOWED_HOSTS` | `your-app.railway.app` (Railway gives you this URL) |
| `DEBUG` | `false` |

### 1.3 Get your Railway URL

After deploy, Railway gives you a URL like:
`https://aie-twin-production.up.railway.app`

**Copy it — you need it in step 3.**

### 1.4 Verify backend is running

```bash
curl https://your-app.railway.app/health
# → {"status": "ok"}
```

---

## Step 2 — Deploy the frontend to Cloudflare Pages

### 2.1 Create Pages project

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **Pages** → **Create a project**
2. Choose **Upload assets** (simplest — no build step needed)
3. Upload these files:
   - `index.html`
   - `_headers`
   - `_redirects`

Or connect your GitHub repo and set:
- **Build command:** *(leave empty)*
- **Build output directory:** `/` (root)

### 2.2 Get your Pages URL

Cloudflare gives you: `https://aie-twin-abc123.pages.dev`

---

## Step 3 — Wire them together

### 3.1 Update PROXY_URL in index.html

Open `index.html` and replace the placeholder:

```js
// Before:
const PROXY_URL = 'RAILWAY_BACKEND_URL/api/chat';

// After (your actual Railway URL):
const PROXY_URL = 'https://aie-twin-production.up.railway.app/api/chat';
```

Make sure `USE_PROXY` is `true`:
```js
const USE_PROXY = true;
```

### 3.2 Update ALLOWED_ORIGINS on Railway

Go back to Railway → Variables, update:
```
ALLOWED_ORIGINS=https://aie-twin-abc123.pages.dev
```

If you have a custom domain, add it too:
```
ALLOWED_ORIGINS=https://aie-twin-abc123.pages.dev,https://yourdomain.com
```

Railway redeploys automatically when you save variables.

### 3.3 Re-upload index.html to Cloudflare Pages

Upload the updated `index.html` with the correct `PROXY_URL`.

---

## Step 4 — Verify end-to-end

1. Open your Pages URL
2. Complete the onboarding (name, role, stack)
3. The briefing should load — Haiku picks sessions, loading messages rotate
4. Open modal on a pick → twin take should appear

If something fails, check:
- Railway logs: **your service → Logs tab**
- Browser console: CORS errors mean `ALLOWED_ORIGINS` doesn't match your Pages URL

---

## Local development

```bash
# Backend
cd aie-twin/
cp .env.example .env
# edit .env — add your ANTHROPIC_KEY
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000

# Frontend — in another terminal, serve index.html on port 3000
# (any static server works)
python3 -m http.server 3000

# Then open http://localhost:3000
# PROXY_URL should be 'http://localhost:8000/api/chat'
```

For local dev, temporarily set in `index.html`:
```js
const USE_PROXY = true;
const PROXY_URL = 'http://localhost:8000/api/chat';
```

---

## Custom domain (optional)

**Cloudflare Pages custom domain:**
Pages → your project → Custom domains → Add domain

**Railway custom domain:**
Railway → your service → Settings → Networking → Custom domain

If you add a custom domain, update `ALLOWED_ORIGINS` on Railway accordingly.

---

## Railway free tier limits

Railway free tier includes $5/month of usage credit.
The backend is idle most of the time — for a 3-day conference app this is plenty.

If you expect heavy traffic, upgrade to the Hobby plan ($5/mo flat).

---

## File structure

```
aie-twin/
├── index.html          ← Cloudflare Pages (the whole frontend)
├── _headers            ← CF Pages security headers
├── _redirects          ← CF Pages SPA routing
├── .env.example        ← copy to .env for local dev
├── .gitignore
├── Procfile            ← Railway start command
├── railway.toml        ← Railway build + health check config
├── nixpacks.toml       ← Railway Python environment
└── backend/
    ├── __init__.py
    ├── main.py         ← Starlette 1.0 app
    ├── requirements.txt
    └── test_main.py    ← pytest suite
```
