# 🚀 Deploy VagaCore Website to Netlify

Your VagaCore landing page is ready to deploy! Follow these simple steps:

---

## ✅ Prerequisites

1. **GitHub Account** - [Sign up](https://github.com) if you don't have one
2. **Netlify Account** - [Sign up](https://netlify.com) (can use GitHub login)

---

## 📤 Step 1: Push to GitHub

If you haven't already pushed your code to GitHub:

```bash
# Navigate to project directory
cd d:\vagacore

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "feat: add landing page and deployment config"

# Create a new repository on GitHub (https://github.com/new)
# Then connect and push:
git remote add origin https://github.com/CHIRABRATA/vagacore.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy to Netlify (3 Methods)

### Method A: Netlify UI (Easiest) ⭐ Recommended

1. **Go to Netlify Dashboard**
   - Visit: [https://app.netlify.com](https://app.netlify.com)
   - Log in with your GitHub account

2. **Import Project**
   - Click **"Add new site"** → **"Import an existing project"**
   - Click **"Deploy with GitHub"**
   - Authorize Netlify to access your repositories
   - Select your `vagacore` repository

3. **Configure Build Settings**
   
   Netlify will auto-detect settings from `netlify.toml`, but verify:
   
   ```
   Site name: vagacore (or your preferred name)
   Branch to deploy: main
   Base directory: (leave empty)
   Build command: echo 'No build needed'
   Publish directory: frontend
   ```

4. **Deploy!**
   - Click **"Deploy site"**
   - Wait 30-60 seconds for deployment
   - Your site will be live at: `https://vagacore.netlify.app`

5. **Custom Domain (Optional)**
   - Go to **Site settings** → **Domain management**
   - Click **"Add custom domain"**
   - Follow instructions to set up your domain

---

### Method B: Netlify CLI (For Developers)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize Netlify site
netlify init

# Follow the prompts:
# - Create & configure a new site
# - Team: THE CHIRABRATA
# - Site name: vagacore
# - Build command: (leave empty or press Enter)
# - Publish directory: frontend

# Deploy
netlify deploy --prod
```

---

### Method C: Drag & Drop (No GitHub Required)

1. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag the `frontend` folder into the browser window
3. Your site deploys instantly!
4. Note: Manual updates required (no auto-deploy from git)

---

## 🎯 Netlify Dashboard Settings

Based on your screenshot, here's what to enter:

| Setting | Value |
|---------|-------|
| **Team** | THE CHIRABRATA |
| **Project Name** | vagacore |
| **Site URL** | `https://vagacore.netlify.app` |
| **Branch to deploy** | `main` |
| **Base directory** | *(leave empty)* |
| **Build command** | *(leave empty or `echo 'No build needed'`)* |
| **Publish directory** | `frontend` |
| **Functions directory** | *(leave empty)* |

---

## 🔄 Auto-Deploy Setup

Once connected to GitHub, Netlify will automatically:

✅ Deploy when you push to `main` branch  
✅ Create preview deployments for pull requests  
✅ Show build logs and deployment status  
✅ Provide HTTPS automatically  

---

## 🧪 Test Your Deployment

After deployment:

1. **Visit your site**: `https://vagacore.netlify.app`
2. **Check all sections load correctly**
3. **Test the interactive demo** (if you have one)
4. **Test on mobile devices**

---

## 🛠️ Troubleshooting

### Issue: 404 Error

**Solution**: Check publish directory is set to `frontend`

```toml
# In netlify.toml
[build]
  publish = "frontend"
```

### Issue: Build Fails

**Solution**: Use this build command:

```bash
echo 'No build needed'
```

### Issue: Wrong Domain

**Solution**: Go to **Site settings** → **Domain management** → **Change site name**

---

## 📊 Environment Variables (If Needed)

If your site needs API keys or secrets:

1. Go to **Site settings** → **Environment variables**
2. Add variables (they won't be exposed in the browser)
3. Access in build: `process.env.VARIABLE_NAME`

---

## 🎨 Custom Domain Setup

### Option 1: Netlify Subdomain (Free)

- Default: `https://vagacore.netlify.app`
- Change name: **Site settings** → **Domain management** → **Options** → **Edit site name**

### Option 2: Custom Domain

1. **Buy a domain** (Namecheap, GoDaddy, etc.)
2. **Add domain in Netlify**:
   - **Site settings** → **Domain management** → **Add custom domain**
   - Enter your domain (e.g., `vagacore.com`)
3. **Update DNS**:
   - Add Netlify's nameservers to your domain registrar
   - Or add A/CNAME records as instructed
4. **Wait for DNS propagation** (5 mins - 48 hours)
5. **HTTPS** is automatic and free!

---

## 🚀 Deployment Checklist

Before deploying, ensure:

- [ ] `frontend/index.html` exists and is working
- [ ] `netlify.toml` is in project root
- [ ] Code is pushed to GitHub (`main` branch)
- [ ] All images/assets are in `frontend/` folder
- [ ] No hardcoded localhost URLs
- [ ] Links are relative (e.g., `./styles.css` not `/styles.css`)

---

## 📈 After Deployment

**Share your site:**
```
🚀 VagaCore is live!
🌐 https://vagacore.netlify.app
⭐ Star on GitHub: https://github.com/CHIRABRATA/vagacore
```

**Monitor your site:**
- Check **Netlify Dashboard** for analytics
- View deployment logs
- Set up form submissions (if using Netlify Forms)
- Enable Netlify Analytics (paid feature)

---

## 🆘 Need Help?

- **Netlify Docs**: [https://docs.netlify.com](https://docs.netlify.com)
- **Netlify Support**: [https://answers.netlify.com](https://answers.netlify.com)
- **Community**: Netlify Discord

---

## ✅ Quick Deploy Commands

```bash
# Push to GitHub
git add .
git commit -m "ready to deploy"
git push origin main

# Netlify will auto-deploy!
# Check status: https://app.netlify.com
```

That's it! Your VagaCore landing page will be live in under a minute! 🎉
