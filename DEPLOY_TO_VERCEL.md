# 🚀 Deploying Social Detective to Vercel

This project is configured out-of-the-box for serverless deployment on [Vercel](https://vercel.com) using Python Serverless Functions.

---

## 📁 Pre-Configured Files

The following configuration files are already set up and tested:
1. **[`api/index.py`](file:///d:/CLG/DS%20project/api/index.py)**: Serverless function entrypoint exposing Flask's `app`.
2. **[`vercel.json`](file:///d:/CLG/DS%20project/vercel.json)**: Rewrites all incoming routes (`/(.*)`) to the serverless entrypoint.
3. **[`.vercelignore`](file:///d:/CLG/DS%20project/.vercelignore)**: Excludes caches, test files, and local logs from deployment.
4. **[`requirements.txt`](file:///d:/CLG/DS%20project/requirements.txt)**: Specifies production dependencies (`Flask`, `gunicorn`, `pytest`).

---

## 🛠️ Deployment Methods

### Method 1: Drag & Drop via Vercel Drop (Easiest — No Git or CLI needed! ⚡)

1. Open **[vercel.com/drop](https://vercel.com/drop)** in your web browser.
2. Log in with your Vercel account (free).
3. **Drag and drop the entire `DS project` folder** (or a `.zip` of it) directly onto the browser window.
   > **Note**: Drop the root folder containing `vercel.json`, `api/`, `templates/`, and `requirements.txt` — not an individual subfolder.
4. Give your project a name (e.g. `social-detective`) and click **Deploy**.
5. Vercel automatically detects the Python configuration and provides your live production link!

---

### Method 2: Push to GitHub & Import into Vercel (Best for Continuous Updates)

1. **Initialize Git and Commit**:
   ```bash
   git init
   git add .
   git commit -m "feat: warm beige editorial theme & Vercel deployment setup"
   ```

2. **Push to your GitHub repository**:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new).
   - Select and import your GitHub repository.
   - Leave the **Framework Preset** as **Other** (Vercel automatically detects `vercel.json` and Python runtime).
   - Click **Deploy**.

---

### Method 2: Deploy Directly via Vercel CLI

If you prefer deploying straight from your terminal:

1. **Run the Vercel CLI**:
   ```bash
   npx vercel
   ```
   *(Or install globally via `npm install -g vercel` and run `vercel`)*

2. **Follow the Prompts**:
   - `Set up and deploy?`: **Y**
   - `Which scope?`: Select your personal or team account
   - `Link to existing project?`: **N**
   - `What's your project's name?`: `social-detective` (or your preferred name)
   - `In which directory is your code located?`: `./`

3. **Deploy to Production**:
   ```bash
   npx vercel --prod
   ```

---

## 🔍 Local Verification

To run and verify the app locally before deployment:
```bash
python app.py
```
Visit: `http://127.0.0.1:5000`

To run all 23 unit and integration tests:
```bash
python -m pytest
```
